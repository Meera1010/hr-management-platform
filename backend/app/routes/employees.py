from flask import Blueprint, request, jsonify
from app import db
from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import or_

employees_bp = Blueprint('employees', __name__)

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

def can_view_employee(current_user, employee_id=None, employee=None):
    if current_user.role.name in ['Admin', 'HR', 'Recruiter']:
        return True
    if current_user.role.name == 'Employee':
        if employee:
            return employee.user_id == current_user.id
        if employee_id:
            emp = Employee.query.get(employee_id)
            return emp and emp.user_id == current_user.id
    return False

def can_manage_employee(current_user):
    return current_user.role.name in ['Admin', 'HR']

@employees_bp.route('/', methods=['GET'])
@jwt_required()
def get_employees():
    current_user = get_current_user()
    
    if current_user.role.name in ['Candidate', 'Interviewer']:
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    # Query parameters for filtering and pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    department_id = request.args.get('department_id', type=int)
    employment_type = request.args.get('employment_type')
    status = request.args.get('status')
    
    query = Employee.query
    
    if current_user.role.name == 'Employee':
        query = query.filter_by(user_id=current_user.id)
    else:
        if department_id:
            query = query.filter_by(department_id=department_id)
        if employment_type:
            query = query.filter_by(employment_type=employment_type)
        if status:
            query = query.filter_by(status=status)
            
    # Pagination
    pagination = query.order_by(Employee.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    employees = pagination.items
    
    return jsonify({
        "success": True,
        "data": {
            "employees": [emp.to_dict() for emp in employees],
            "current_page": pagination.page,
            "total_pages": pagination.pages,
            "total_records": pagination.total
        }
    }), 200

@employees_bp.route('/search', methods=['GET'])
@jwt_required()
def search_employees():
    current_user = get_current_user()
    
    if current_user.role.name in ['Candidate', 'Interviewer', 'Employee']:
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    query_term = request.args.get('q', '')
    if not query_term:
        return jsonify({"success": True, "data": []}), 200
        
    search = f"%{query_term}%"
    employees = Employee.query.filter(
        or_(
            Employee.employee_code.ilike(search),
            Employee.first_name.ilike(search),
            Employee.last_name.ilike(search),
            Employee.email.ilike(search),
            Employee.designation.ilike(search)
        )
    ).all()
    
    return jsonify({
        "success": True,
        "data": [emp.to_dict() for emp in employees]
    }), 200

@employees_bp.route('/department/<int:department_id>', methods=['GET'])
@jwt_required()
def get_employees_by_department(department_id):
    current_user = get_current_user()
    if not can_view_employee(current_user):
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    employees = Employee.query.filter_by(department_id=department_id).all()
    return jsonify({
        "success": True,
        "data": [emp.to_dict() for emp in employees]
    }), 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    current_user = get_current_user()
    employee = Employee.query.get_or_404(employee_id)
    
    if not can_view_employee(current_user, employee=employee):
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    return jsonify({
        "success": True,
        "data": employee.to_dict()
    }), 200

@employees_bp.route('/', methods=['POST'])
@jwt_required()
def create_employee():
    current_user = get_current_user()
    if not can_manage_employee(current_user):
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    required_fields = ['employee_code', 'first_name', 'last_name', 'email', 'department_id', 'designation', 'joining_date', 'employment_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"{field} is required"}), 400
            
    if Employee.query.filter_by(employee_code=data['employee_code']).first():
        return jsonify({"success": False, "message": "Employee code already exists"}), 409
        
    if Employee.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "message": "Email already exists"}), 409
        
    if not Department.query.get(data['department_id']):
        return jsonify({"success": False, "message": "Invalid department_id"}), 400
        
    valid_types = ['Full Time', 'Part Time', 'Contract', 'Intern']
    if data['employment_type'] not in valid_types:
        return jsonify({"success": False, "message": "Invalid employment_type"}), 400
        
    try:
        joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"success": False, "message": "joining_date must be YYYY-MM-DD format"}), 400
        
    # Attempt to link to user record by email
    user = User.query.filter_by(email=data['email']).first()
    
    employee = Employee(
        employee_code=data['employee_code'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        department_id=data['department_id'],
        user_id=user.id if user else None,
        designation=data['designation'],
        joining_date=joining_date,
        employment_type=data['employment_type'],
        status=data.get('status', 'Active')
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Employee created successfully",
        "data": employee.to_dict()
    }), 201

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    current_user = get_current_user()
    if not can_manage_employee(current_user):
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    if 'employee_code' in data and data['employee_code'] != employee.employee_code:
        if Employee.query.filter_by(employee_code=data['employee_code']).first():
            return jsonify({"success": False, "message": "Employee code already exists"}), 409
        employee.employee_code = data['employee_code']
        
    if 'email' in data and data['email'] != employee.email:
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({"success": False, "message": "Email already exists"}), 409
        employee.email = data['email']
        
    if 'department_id' in data:
        if not Department.query.get(data['department_id']):
            return jsonify({"success": False, "message": "Invalid department_id"}), 400
        employee.department_id = data['department_id']
        
    if 'employment_type' in data:
        valid_types = ['Full Time', 'Part Time', 'Contract', 'Intern']
        if data['employment_type'] not in valid_types:
            return jsonify({"success": False, "message": "Invalid employment_type"}), 400
        employee.employment_type = data['employment_type']
        
    if 'status' in data:
        valid_statuses = ['Active', 'Inactive', 'On Leave']
        if data['status'] not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        employee.status = data['status']
        
    if 'joining_date' in data:
        try:
            employee.joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"success": False, "message": "joining_date must be YYYY-MM-DD format"}), 400
            
    employee.first_name = data.get('first_name', employee.first_name)
    employee.last_name = data.get('last_name', employee.last_name)
    employee.phone = data.get('phone', employee.phone)
    employee.designation = data.get('designation', employee.designation)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Employee updated successfully",
        "data": employee.to_dict()
    }), 200

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def deactivate_employee(employee_id):
    current_user = get_current_user()
    if not can_manage_employee(current_user):
        return jsonify({"success": False, "message": "Access denied"}), 403
        
    employee = Employee.query.get_or_404(employee_id)
    employee.status = 'Inactive'
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Employee deactivated successfully",
        "data": employee.to_dict()
    }), 200
