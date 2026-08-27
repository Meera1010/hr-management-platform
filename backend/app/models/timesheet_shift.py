from datetime import datetime
from app import db

class Timesheet(db.Model):
    __tablename__ = 'timesheets'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    week_end_date = db.Column(db.Date, nullable=False)
    total_hours = db.Column(db.Float, default=0.0)
    billable_hours = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Submitted')  # Draft, Submitted, Approved, Rejected
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approver_comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='timesheets', lazy=True)
    entries = db.relationship('TimesheetEntry', backref='timesheet', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'week_start_date': self.week_start_date.strftime('%Y-%m-%d') if self.week_start_date else None,
            'week_end_date': self.week_end_date.strftime('%Y-%m-%d') if self.week_end_date else None,
            'total_hours': self.total_hours,
            'billable_hours': self.billable_hours,
            'status': self.status,
            'approver_comments': self.approver_comments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'entries': [e.to_dict() for e in self.entries]
        }


class TimesheetEntry(db.Model):
    __tablename__ = 'timesheet_entries'

    id = db.Column(db.Integer, primary_key=True)
    timesheet_id = db.Column(db.Integer, db.ForeignKey('timesheets.id'), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    project_name = db.Column(db.String(150), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    hours_logged = db.Column(db.Float, default=0.0)
    is_billable = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'timesheet_id': self.timesheet_id,
            'entry_date': self.entry_date.strftime('%Y-%m-%d') if self.entry_date else None,
            'project_name': self.project_name,
            'task_description': self.task_description,
            'hours_logged': self.hours_logged,
            'is_billable': self.is_billable
        }


class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Morning Shift, General Shift, Night Shift, Weekend Roster
    code = db.Column(db.String(30), unique=True, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)  # e.g., "09:00"
    end_time = db.Column(db.String(10), nullable=False)    # e.g., "18:00"
    break_duration_mins = db.Column(db.Integer, default=60)
    is_night_shift = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    rosters = db.relationship('EmployeeShiftRoster', backref='shift', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'break_duration_mins': self.break_duration_mins,
            'is_night_shift': self.is_night_shift,
            'is_active': self.is_active
        }


class EmployeeShiftRoster(db.Model):
    __tablename__ = 'employee_shift_rosters'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    roster_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Scheduled')  # Scheduled, Swapped, Cancelled, Completed

    employee = db.relationship('Employee', backref='shift_rosters', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'shift_id': self.shift_id,
            'shift_name': self.shift.name if self.shift else None,
            'shift_start': self.shift.start_time if self.shift else None,
            'shift_end': self.shift.end_time if self.shift else None,
            'roster_date': self.roster_date.strftime('%Y-%m-%d') if self.roster_date else None,
            'status': self.status
        }


class OvertimeClaim(db.Model):
    __tablename__ = 'overtime_claims'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    claim_date = db.Column(db.Date, nullable=False)
    ot_hours = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    hourly_rate = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Submitted')  # Submitted, Approved, Rejected, Paid
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='overtime_claims', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'claim_date': self.claim_date.strftime('%Y-%m-%d') if self.claim_date else None,
            'ot_hours': self.ot_hours,
            'reason': self.reason,
            'hourly_rate': self.hourly_rate,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
