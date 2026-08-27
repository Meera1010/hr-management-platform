import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.utils.auth import role_required

logger = logging.getLogger('audit')
leaves_bp = Blueprint('leaves', __name__)


def _get_employee_for_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return Employee.query.filter_by(user_id=user.id).first()


# ─── LIST ──────────────────────────────────────────────────────────────────────

@leaves_bp.route('', methods=['GET'])
@jwt_required()
def get_leaves():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role in ('Admin', 'HR'):
        status_filter = request.args.get('status')
        emp_filter = request.args.get('employee_id')
        query = LeaveRequest.query
        if status_filter:
            query = query.filter_by(status=status_filter)
        if emp_filter:
            query = query.filter_by(employee_id=int(emp_filter))
        leaves = query.order_by(LeaveRequest.created_at.desc()).all()
        return jsonify({'success': True, 'data': [l.to_dict() for l in leaves]})

    elif role == 'Employee':
        emp = _get_employee_for_user(user_id)
        if not emp:
            return jsonify({'success': True, 'data': []})
        leaves = LeaveRequest.query.filter_by(employee_id=emp.id).order_by(LeaveRequest.created_at.desc()).all()
        return jsonify({'success': True, 'data': [l.to_dict() for l in leaves]})

    else:
        return jsonify({'success': False, 'message': 'Forbidden'}), 403


# ─── GET SINGLE ───────────────────────────────────────────────────────────────

@leaves_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_leave(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    leave = LeaveRequest.query.get(id)
    if not leave:
        return jsonify({'success': False, 'message': 'Leave request not found'}), 404

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or leave.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403

    return jsonify({'success': True, 'data': leave.to_dict()})


# ─── CREATE LEAVE (Employee) ───────────────────────────────────────────────────

@leaves_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Employee')
def create_leave():
    user_id = get_jwt_identity()
    emp = _get_employee_for_user(user_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee record not found for your account'}), 404

    data = request.get_json() or {}
    leave_type = data.get('leave_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    reason = data.get('reason', '').strip()

    if not leave_type or leave_type not in LeaveRequest.LEAVE_TYPES:
        return jsonify({'success': False, 'message': f"leave_type must be one of: {', '.join(LeaveRequest.LEAVE_TYPES)}"}), 400
    if not start_date:
        return jsonify({'success': False, 'message': 'start_date is required'}), 400
    if not end_date:
        return jsonify({'success': False, 'message': 'end_date is required'}), 400
    if end_date < start_date:
        return jsonify({'success': False, 'message': 'end_date cannot be before start_date'}), 400
    if not reason:
        return jsonify({'success': False, 'message': 'reason is required'}), 400

    last = LeaveRequest.query.order_by(LeaveRequest.id.desc()).first()
    next_num = (last.id + 1) if last else 1
    leave_code = f"LVE-{next_num:04d}"

    leave = LeaveRequest(
        leave_code=leave_code,
        employee_id=emp.id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status='Pending'
    )
    db.session.add(leave)
    db.session.commit()
    logger.info(f"Audit: Leave requested. Code: {leave_code}, Employee ID: {emp.id}, Type: {leave_type}")
    return jsonify({'success': True, 'message': 'Leave request submitted', 'data': leave.to_dict()}), 201


# ─── UPDATE LEAVE (Employee can edit own Pending leave) ───────────────────────

@leaves_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_leave(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    leave = LeaveRequest.query.get(id)
    if not leave:
        return jsonify({'success': False, 'message': 'Leave request not found'}), 404

    if role == 'Employee':
        emp = _get_employee_for_user(user_id)
        if not emp or leave.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403
        if leave.status != 'Pending':
            return jsonify({'success': False, 'message': 'Can only edit Pending leave requests'}), 400
    elif role not in ('Admin', 'HR'):
        return jsonify({'success': False, 'message': 'Forbidden'}), 403

    data = request.get_json() or {}
    if 'leave_type' in data:
        if data['leave_type'] not in LeaveRequest.LEAVE_TYPES:
            return jsonify({'success': False, 'message': 'Invalid leave_type'}), 400
        leave.leave_type = data['leave_type']
    if 'start_date' in data:
        leave.start_date = data['start_date']
    if 'end_date' in data:
        leave.end_date = data['end_date']
    if leave.end_date < leave.start_date:
        return jsonify({'success': False, 'message': 'end_date cannot be before start_date'}), 400
    if 'reason' in data:
        leave.reason = data['reason']

    db.session.commit()
    return jsonify({'success': True, 'message': 'Leave request updated', 'data': leave.to_dict()})


# ─── APPROVE ──────────────────────────────────────────────────────────────────

@leaves_bp.route('/<int:id>/approve', methods=['PATCH'])
@jwt_required()
@role_required('Admin', 'HR')
def approve_leave(id):
    user_id = get_jwt_identity()
    leave = LeaveRequest.query.get(id)
    if not leave:
        return jsonify({'success': False, 'message': 'Leave request not found'}), 404
    if leave.status != 'Pending':
        return jsonify({'success': False, 'message': f"Cannot approve a leave in '{leave.status}' status"}), 400

    data = request.get_json() or {}
    leave.status = 'Approved'
    leave.manager_comment = data.get('manager_comment', 'Approved')
    db.session.commit()
    logger.info(f"Audit: Leave approved. ID: {id}, Employee ID: {leave.employee_id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Leave approved', 'data': leave.to_dict()})


# ─── REJECT ───────────────────────────────────────────────────────────────────

@leaves_bp.route('/<int:id>/reject', methods=['PATCH'])
@jwt_required()
@role_required('Admin', 'HR')
def reject_leave(id):
    user_id = get_jwt_identity()
    leave = LeaveRequest.query.get(id)
    if not leave:
        return jsonify({'success': False, 'message': 'Leave request not found'}), 404
    if leave.status != 'Pending':
        return jsonify({'success': False, 'message': f"Cannot reject a leave in '{leave.status}' status"}), 400

    data = request.get_json() or {}
    leave.status = 'Rejected'
    leave.manager_comment = data.get('manager_comment', 'Rejected')
    db.session.commit()
    logger.info(f"Audit: Leave rejected. ID: {id}, Employee ID: {leave.employee_id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Leave rejected', 'data': leave.to_dict()})


# ─── CANCEL (Employee cancels own Pending leave) ───────────────────────────────

@leaves_bp.route('/<int:id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_leave(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    leave = LeaveRequest.query.get(id)
    if not leave:
        return jsonify({'success': False, 'message': 'Leave request not found'}), 404

    if role == 'Employee':
        emp = _get_employee_for_user(user_id)
        if not emp or leave.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403
    elif role not in ('Admin', 'HR'):
        return jsonify({'success': False, 'message': 'Forbidden'}), 403

    if leave.status not in ('Pending',):
        return jsonify({'success': False, 'message': 'Only Pending leaves can be cancelled'}), 400

    leave.status = 'Cancelled'
    db.session.commit()
    logger.info(f"Audit: Leave cancelled. ID: {id}, Employee ID: {leave.employee_id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Leave cancelled', 'data': leave.to_dict()})


# ─── EMPLOYEE LEAVES ──────────────────────────────────────────────────────────

@leaves_bp.route('/employee/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_leaves(employee_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or emp.id != employee_id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403

    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

    leaves = LeaveRequest.query.filter_by(employee_id=employee_id).order_by(LeaveRequest.created_at.desc()).all()
    return jsonify({'success': True, 'data': [l.to_dict() for l in leaves]})
