from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.timesheet_shift import Timesheet, TimesheetEntry, Shift, EmployeeShiftRoster, OvertimeClaim
from app.services.timesheet_service import TimesheetService
from app.utils.auth import token_required, role_required

timesheets_bp = Blueprint('timesheets', __name__)

@timesheets_bp.route('/weekly', methods=['GET'])
@token_required
def get_timesheets(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        timesheets = Timesheet.query.order_by(Timesheet.week_start_date.desc()).all()
    else:
        if not emp:
            return jsonify({'timesheets': []}), 200
        timesheets = Timesheet.query.filter_by(employee_id=emp.id).order_by(Timesheet.week_start_date.desc()).all()

    return jsonify({'timesheets': [t.to_dict() for t in timesheets]}), 200

@timesheets_bp.route('/weekly', methods=['POST'])
@token_required
def create_timesheet(current_user):
    data = request.get_json() or {}
    start_date_str = data.get('week_start_date')
    end_date_str = data.get('week_end_date')

    if not start_date_str or not end_date_str:
        return jsonify({'message': 'week_start_date and week_end_date are required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    s_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    e_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    timesheet = Timesheet(
        employee_id=emp_id,
        week_start_date=s_date,
        week_end_date=e_date,
        status='Submitted'
    )
    db.session.add(timesheet)
    db.session.commit()

    entries_data = data.get('entries', [])
    for item in entries_data:
        entry_d = datetime.strptime(item.get('entry_date', start_date_str), '%Y-%m-%d').date()
        e = TimesheetEntry(
            timesheet_id=timesheet.id,
            entry_date=entry_d,
            project_name=item.get('project_name', 'General'),
            task_description=item.get('task_description'),
            hours_logged=float(item.get('hours_logged', 0.0)),
            is_billable=bool(item.get('is_billable', True))
        )
        db.session.add(e)

    db.session.commit()
    TimesheetService.recalculate_timesheet_totals(timesheet.id)
    return jsonify({'message': 'Timesheet submitted successfully', 'timesheet': timesheet.to_dict()}), 201


@timesheets_bp.route('/shifts', methods=['GET'])
@token_required
def get_shifts(current_user):
    shifts = Shift.query.all()
    return jsonify({'shifts': [s.to_dict() for s in shifts]}), 200

@timesheets_bp.route('/shifts', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_shift(current_user):
    data = request.get_json() or {}
    if not data.get('name') or not data.get('code'):
        return jsonify({'message': 'Shift name and code are required'}), 400

    start_t = datetime.strptime(data.get('start_time', '09:00'), '%H:%M').time()
    end_t = datetime.strptime(data.get('end_time', '18:00'), '%H:%M').time()

    shift = Shift(
        name=data['name'],
        code=data['code'],
        start_time=start_t,
        end_time=end_t,
        break_duration_minutes=int(data.get('break_duration_minutes', 60))
    )
    db.session.add(shift)
    db.session.commit()
    return jsonify({'message': 'Shift created successfully', 'shift': shift.to_dict()}), 201

@timesheets_bp.route('/rosters', methods=['GET'])
@token_required
def get_rosters(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        rosters = EmployeeShiftRoster.query.order_by(EmployeeShiftRoster.roster_date.desc()).all()
    else:
        if not emp:
            return jsonify({'rosters': []}), 200
        rosters = EmployeeShiftRoster.query.filter_by(employee_id=emp.id).order_by(EmployeeShiftRoster.roster_date.desc()).all()

    return jsonify({'rosters': [r.to_dict() for r in rosters]}), 200

@timesheets_bp.route('/overtime-claims', methods=['GET'])
@token_required
def get_overtime_claims(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        claims = OvertimeClaim.query.all()
    else:
        if not emp:
            return jsonify({'claims': []}), 200
        claims = OvertimeClaim.query.filter_by(employee_id=emp.id).all()

    return jsonify({'claims': [c.to_dict() for c in claims]}), 200
