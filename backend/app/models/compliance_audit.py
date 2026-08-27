from datetime import datetime
from app import db

class GrievanceTicket(db.Model):
    __tablename__ = 'grievance_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False)
    raised_by_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)  # Null if anonymous
    is_anonymous = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), default='Workplace Conduct')  # Workplace Conduct, Compensation, Harassment, Policy, Discrimination, Other
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Critical
    status = db.Column(db.String(30), default='Open')      # Open, Under Investigation, Resolved, Closed
    assigned_hr_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolution_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    employee = db.relationship('Employee', backref='grievances', lazy=True)
    logs = db.relationship('GrievanceLog', backref='ticket', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'raised_by_employee_id': self.raised_by_employee_id if not self.is_anonymous else None,
            'raised_by_name': "Anonymous" if self.is_anonymous else (f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None),
            'is_anonymous': self.is_anonymous,
            'category': self.category,
            'subject': self.subject,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'resolution_summary': self.resolution_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'logs': [l.to_dict() for l in self.logs]
        }


class GrievanceLog(db.Model):
    __tablename__ = 'grievance_logs'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('grievance_tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    note = db.Column(db.Text, nullable=False)
    status_changed_to = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'note': self.note,
            'status_changed_to': self.status_changed_to,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CompanyPolicy(db.Model):
    __tablename__ = 'company_policies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    category = db.Column(db.String(50), default='General HR')  # Code of Conduct, IT & Data Security, POSH, Leave & Attendance, Remote Work
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.String(20), default='1.0')
    is_mandatory_acknowledgment = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    effective_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    acknowledgments = db.relationship('PolicyAcknowledgment', backref='policy', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'category': self.category,
            'content': self.content,
            'version': self.version,
            'is_mandatory_acknowledgment': self.is_mandatory_acknowledgment,
            'is_active': self.is_active,
            'effective_date': self.effective_date.strftime('%Y-%m-%d') if self.effective_date else None
        }


class PolicyAcknowledgment(db.Model):
    __tablename__ = 'policy_acknowledgments'

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('company_policies.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    acknowledged_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=True)

    employee = db.relationship('Employee', backref='policy_acknowledgments', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'policy_id': self.policy_id,
            'policy_title': self.policy.title if self.policy else None,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_email = db.Column(db.String(120), nullable=True)
    action = db.Column(db.String(100), nullable=False)      # CREATE, UPDATE, DELETE, LOGIN, EXPORT
    entity_type = db.Column(db.String(100), nullable=False) # Employee, Salary, Job, Offer, Asset
    entity_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_email': self.user_email,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
