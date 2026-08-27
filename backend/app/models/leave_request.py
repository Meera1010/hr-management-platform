from datetime import datetime
from app import db


class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    LEAVE_TYPES = ['Casual', 'Annual', 'Unpaid', 'Personal']
    STATUSES = ['Pending', 'Approved', 'Rejected', 'Cancelled']

    id = db.Column(db.Integer, primary_key=True)
    leave_code = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    leave_type = db.Column(db.String(50), nullable=False)     # Casual, Annual, Unpaid, Personal
    start_date = db.Column(db.String(20), nullable=False)     # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=False)       # YYYY-MM-DD
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    # Status: Pending, Approved, Rejected, Cancelled
    manager_comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('Employee', backref=db.backref('leave_requests', lazy=True, cascade='all, delete-orphan'))

    @property
    def days_count(self):
        """Calculate number of leave days (inclusive)."""
        try:
            from datetime import date
            start = date.fromisoformat(self.start_date)
            end = date.fromisoformat(self.end_date)
            return max(1, (end - start).days + 1)
        except (ValueError, TypeError):
            return 1

    def to_dict(self):
        return {
            'id': self.id,
            'leave_code': self.leave_code,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_code': self.employee.employee_code if self.employee else None,
            'department_name': self.employee.department.name if self.employee and self.employee.department else None,
            'leave_type': self.leave_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'days_count': self.days_count,
            'reason': self.reason,
            'status': self.status,
            'manager_comment': self.manager_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
