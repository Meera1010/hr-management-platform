import logging
from datetime import date as dt_date, datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.utils.auth import role_required

logger = logging.getLogger('audit')
attendance_bp = Blueprint('attendance', __name__)

VALID_STATUSES = ['Present', 'Absent', 'Half Day', 'Work From Home', 'On Leave']


def _get_employee_for_user(user_id):
    """Return Employee record linked to given user_id, or None."""
    user = User.query.get(user_id)
    if not user:
        return None
    return Employee.query.filter_by(user_id=user.id).first()


# ─── LIST ALL (HR/Admin) OR OWN (Employee) ────────────────────────────────────

@attendance_bp.route('', methods=['GET'])
@jwt_required()
def get_attendances():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role in ('Admin', 'HR'):
        emp_id = request.args.get('employee_id')
        att_date = request.args.get('date')
        status = request.args.get('status')

        query = Attendance.query
        if emp_id:
            query = query.filter_by(employee_id=int(emp_id))
        if att_date:
            query = query.filter_by(attendance_date=att_date)
        if status:
            query = query.filter_by(status=status)

        records = query.order_by(Attendance.attendance_date.desc()).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in records]})

    elif role == 'Employee':
        emp = _get_employee_for_user(user_id)
        if not emp:
            return jsonify({'success': True, 'data': []})
        records = Attendance.query.filter_by(employee_id=emp.id).order_by(Attendance.attendance_date.desc()).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in records]})

    else:
        return jsonify({'success': False, 'message': 'Forbidden'}), 403


# ─── GET SINGLE ───────────────────────────────────────────────────────────────

@attendance_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_attendance(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    record = Attendance.query.get(id)
    if not record:
        return jsonify({'success': False, 'message': 'Attendance record not found'}), 404

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or record.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403

    return jsonify({'success': True, 'data': record.to_dict()})


# ─── CREATE (HR/Admin manual entry) ───────────────────────────────────────────

@attendance_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR')
def create_attendance():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    employee_id = data.get('employee_id')
    attendance_date = data.get('attendance_date')
    status = data.get('status', 'Present')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    remarks = data.get('remarks', '')

    if not employee_id or not attendance_date:
        return jsonify({'success': False, 'message': 'employee_id and attendance_date are required'}), 400

    if status not in VALID_STATUSES:
        return jsonify({'success': False, 'message': f'Invalid status. Valid: {", ".join(VALID_STATUSES)}'}), 400

    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

    existing = Attendance.query.filter_by(employee_id=employee_id, attendance_date=attendance_date).first()
    if existing:
        return jsonify({'success': False, 'message': 'Attendance record already exists for this employee on this date'}), 400

    work_hours = None
    if check_in and check_out:
        work_hours = Attendance.calculate_work_hours(check_in, check_out)
        if work_hours is None:
            return jsonify({'success': False, 'message': 'check_out must be after check_in'}), 400

    record = Attendance(
        employee_id=int(employee_id),
        attendance_date=attendance_date,
        check_in=check_in,
        check_out=check_out,
        status=status,
        work_hours=work_hours,
        remarks=remarks
    )
    db.session.add(record)
    db.session.commit()
    logger.info(f"Audit: Attendance created manually. Employee ID: {employee_id}, Date: {attendance_date}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Attendance record created', 'data': record.to_dict()}), 201


# ─── UPDATE (HR/Admin) ────────────────────────────────────────────────────────

@attendance_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('Admin', 'HR')
def update_attendance(id):
    user_id = get_jwt_identity()
    record = Attendance.query.get(id)
    if not record:
        return jsonify({'success': False, 'message': 'Attendance record not found'}), 404

    data = request.get_json() or {}

    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({'success': False, 'message': f'Invalid status'}), 400
        record.status = data['status']
    if 'check_in' in data:
        record.check_in = data['check_in']
    if 'check_out' in data:
        record.check_out = data['check_out']
    if 'remarks' in data:
        record.remarks = data['remarks']

    if record.check_in and record.check_out:
        wh = Attendance.calculate_work_hours(record.check_in, record.check_out)
        if wh is None:
            return jsonify({'success': False, 'message': 'check_out must be after check_in'}), 400
        record.work_hours = wh

    db.session.commit()
    logger.info(f"Audit: Attendance updated. ID: {id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Attendance updated', 'data': record.to_dict()})


# ─── DELETE (HR/Admin) ────────────────────────────────────────────────────────

@attendance_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin', 'HR')
def delete_attendance(id):
    user_id = get_jwt_identity()
    record = Attendance.query.get(id)
    if not record:
        return jsonify({'success': False, 'message': 'Attendance record not found'}), 404

    db.session.delete(record)
    db.session.commit()
    logger.info(f"Audit: Attendance deleted. ID: {id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Attendance record deleted'})


# ─── EMPLOYEE ATTENDANCE LIST ──────────────────────────────────────────────────

@attendance_bp.route('/employee/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_attendance(employee_id):
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

    records = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.attendance_date.desc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in records]})


# ─── ATTENDANCE SUMMARY ────────────────────────────────────────────────────────

@attendance_bp.route('/summary/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_attendance_summary(employee_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or emp.id != employee_id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403

    records = Attendance.query.filter_by(employee_id=employee_id).all()
    total = len(records)
    present = sum(1 for r in records if r.status == 'Present')
    absent = sum(1 for r in records if r.status == 'Absent')
    half_day = sum(1 for r in records if r.status == 'Half Day')
    wfh = sum(1 for r in records if r.status == 'Work From Home')
    on_leave = sum(1 for r in records if r.status == 'On Leave')

    working_days = present + absent + half_day + wfh + on_leave
    attendance_pct = round((present / working_days) * 100, 2) if working_days > 0 else 0.0

    return jsonify({
        'success': True,
        'data': {
            'employee_id': employee_id,
            'total_records': total,
            'total_working_days': working_days,
            'present_days': present,
            'absent_days': absent,
            'half_days': half_day,
            'wfh_days': wfh,
            'leave_days': on_leave,
            'attendance_percentage': attendance_pct
        }
    })


# ─── CHECK-IN (Employee self-service) ─────────────────────────────────────────

@attendance_bp.route('/check-in', methods=['POST'])
@jwt_required()
@role_required('Employee')
def check_in():
    user_id = get_jwt_identity()
    emp = _get_employee_for_user(user_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee record not found for your account'}), 404

    today = dt_date.today().isoformat()
    existing = Attendance.query.filter_by(employee_id=emp.id, attendance_date=today).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already checked in today'}), 400

    now_time = datetime.utcnow().strftime('%H:%M:%S')
    record = Attendance(
        employee_id=emp.id,
        attendance_date=today,
        check_in=now_time,
        status='Present'
    )
    db.session.add(record)
    db.session.commit()
    logger.info(f"Audit: Employee checked in. Employee ID: {emp.id}, Date: {today}, Time: {now_time}")
    return jsonify({
        'success': True,
        'message': 'Check-in successful',
        'data': record.to_dict()
    }), 201


# ─── CHECK-OUT (Employee self-service) ────────────────────────────────────────

@attendance_bp.route('/check-out', methods=['POST'])
@jwt_required()
@role_required('Employee')
def check_out():
    user_id = get_jwt_identity()
    emp = _get_employee_for_user(user_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee record not found for your account'}), 404

    today = dt_date.today().isoformat()
    record = Attendance.query.filter_by(employee_id=emp.id, attendance_date=today).first()
    if not record:
        return jsonify({'success': False, 'message': 'You have not checked in today'}), 400
    if record.check_out:
        return jsonify({'success': False, 'message': 'Already checked out today'}), 400

    now_time = datetime.utcnow().strftime('%H:%M:%S')
    work_hours = Attendance.calculate_work_hours(record.check_in, now_time)
    record.check_out = now_time
    record.work_hours = work_hours
    db.session.commit()
    logger.info(f"Audit: Employee checked out. Employee ID: {emp.id}, Date: {today}, Work Hours: {work_hours}")
    return jsonify({
        'success': True,
        'message': 'Check-out successful',
        'data': record.to_dict()
    })
