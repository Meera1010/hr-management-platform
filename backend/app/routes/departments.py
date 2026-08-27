from flask import Blueprint, request, jsonify
from app import db
from app.models.department import Department
from app.models.employee import Employee
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.auth import admin_required, hr_required

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    return jsonify({
        "success": True,
        "data": [dept.to_dict() for dept in departments]
    }), 200

@departments_bp.route('/<int:department_id>', methods=['GET'])
@jwt_required()
def get_department(department_id):
    department = Department.query.get_or_404(department_id)
    return jsonify({
        "success": True,
        "data": department.to_dict()
    }), 200

@departments_bp.route('/', methods=['POST'])
@jwt_required()
@hr_required()
def create_department():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({
            "success": False,
            "message": "Department name is required"
        }), 400
        
    name = data.get('name').strip()
    
    # Check duplicate
    if Department.query.filter_by(name=name).first():
        return jsonify({
            "success": False,
            "message": "Department with this name already exists"
        }), 409
        
    department = Department(
        name=name,
        description=data.get('description', ''),
        status=data.get('status', 'Active')
    )
    
    db.session.add(department)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Department created successfully",
        "data": department.to_dict()
    }), 201

@departments_bp.route('/<int:department_id>', methods=['PUT'])
@jwt_required()
@hr_required()
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    if 'name' in data:
        name = data['name'].strip()
        if not name:
            return jsonify({"success": False, "message": "Department name cannot be empty"}), 400
            
        existing = Department.query.filter_by(name=name).first()
        if existing and existing.id != department_id:
            return jsonify({"success": False, "message": "Department name already exists"}), 409
        department.name = name
        
    if 'description' in data:
        department.description = data['description']
        
    if 'status' in data:
        if data['status'] not in ['Active', 'Inactive']:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        department.status = data['status']
        
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Department updated successfully",
        "data": department.to_dict()
    }), 200

@departments_bp.route('/<int:department_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    
    active_employees = Employee.query.filter_by(department_id=department_id, status='Active').count()
    if active_employees > 0:
        return jsonify({
            "success": False,
            "message": "Cannot deactivate a department with active employees"
        }), 400
        
    department.status = 'Inactive'
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Department deactivated successfully",
        "data": department.to_dict()
    }), 200
