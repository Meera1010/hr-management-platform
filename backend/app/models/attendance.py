from datetime import datetime
from app import db


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    attendance_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    check_in = db.Column(db.String(10), nullable=True)   # HH:MM:SS
    check_out = db.Column(db.String(10), nullable=True)  # HH:MM:SS
    status = db.Column(db.String(30), nullable=False, default='Present')
    # Status: Present, Absent, Half Day, Work From Home, On Leave
    work_hours = db.Column(db.Float, nullable=True)      # Calculated on check-out
    remarks = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('Employee', backref=db.backref('attendances', lazy=True, cascade='all, delete-orphan'))

    __table_args__ = (
        db.UniqueConstraint('employee_id', 'attendance_date', name='uq_employee_date'),
    )

    @staticmethod
    def calculate_work_hours(check_in_str, check_out_str):
        """Calculate work hours from HH:MM or HH:MM:SS strings."""
        if not check_in_str or not check_out_str:
            return None
        try:
            def parse_time(t):
                parts = t.strip().split(':')
                h = int(parts[0])
                m = int(parts[1]) if len(parts) > 1 else 0
                s = int(parts[2]) if len(parts) > 2 else 0
                return h * 3600 + m * 60 + s

            in_secs = parse_time(check_in_str)
            out_secs = parse_time(check_out_str)
            if out_secs <= in_secs:
                return None
            diff_hours = (out_secs - in_secs) / 3600.0
            return round(diff_hours, 2)
        except (ValueError, AttributeError, IndexError):
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_code': self.employee.employee_code if self.employee else None,
            'department_name': self.employee.department.name if self.employee and self.employee.department else None,
            'attendance_date': self.attendance_date,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': self.status,
            'work_hours': self.work_hours,
            'remarks': self.remarks,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
