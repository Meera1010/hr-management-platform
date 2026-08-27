from datetime import datetime
from app import db

class OnboardingChecklist(db.Model):
    __tablename__ = 'onboarding_checklists'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False, default="Employee Onboarding Plan")
    target_completion_date = db.Column(db.Date, nullable=True)
    overall_status = db.Column(db.String(30), default='In Progress')  # Pending, In Progress, Completed
    buddy_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    hr_coordinator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    employee = db.relationship('Employee', foreign_keys=[employee_id], backref='onboarding_checklist', lazy=True)
    buddy = db.relationship('Employee', foreign_keys=[buddy_employee_id], lazy=True)
    tasks = db.relationship('OnboardingTask', backref='checklist', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t.is_completed)
        pct = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0

        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'title': self.title,
            'target_completion_date': self.target_completion_date.strftime('%Y-%m-%d') if self.target_completion_date else None,
            'overall_status': self.overall_status,
            'buddy_name': f"{self.buddy.first_name} {self.buddy.last_name}" if self.buddy else None,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_percentage': pct,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'tasks': [t.to_dict() for t in self.tasks]
        }


class OnboardingTask(db.Model):
    __tablename__ = 'onboarding_tasks'

    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('onboarding_checklists.id'), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='Documentation')  # Documentation, IT Setup, HR Orientation, Training, Manager Sync
    assigned_role = db.Column(db.String(50), default='Employee')  # Employee, HR, IT Admin, Manager
    due_date = db.Column(db.Date, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'checklist_id': self.checklist_id,
            'task_name': self.task_name,
            'category': self.category,
            'assigned_role': self.assigned_role,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }


class EmployeeDocument(db.Model):
    __tablename__ = 'employee_documents'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # ID Proof, Passport, Degree Certificate, Offer Acceptance, Relieving Letter
    document_name = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    verification_status = db.Column(db.String(30), default='Pending')  # Pending, Verified, Rejected
    verified_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='documents', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'document_type': self.document_type,
            'document_name': self.document_name,
            'verification_status': self.verification_status,
            'rejection_reason': self.rejection_reason,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class ResignationRequest(db.Model):
    __tablename__ = 'resignation_requests'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    submission_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    reason = db.Column(db.Text, nullable=False)
    notice_period_days = db.Column(db.Integer, default=60)
    requested_last_working_day = db.Column(db.Date, nullable=False)
    approved_last_working_day = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Submitted')  # Submitted, Under Review, Approved, Rejected, Withdrawn
    manager_comments = db.Column(db.Text, nullable=True)
    hr_comments = db.Column(db.Text, nullable=True)
    exit_interview_conducted = db.Column(db.Boolean, default=False)
    exit_interview_feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('Employee', backref='resignation_requests', lazy=True)
    clearances = db.relationship('ExitClearance', backref='resignation_request', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'submission_date': self.submission_date.strftime('%Y-%m-%d') if self.submission_date else None,
            'reason': self.reason,
            'notice_period_days': self.notice_period_days,
            'requested_last_working_day': self.requested_last_working_day.strftime('%Y-%m-%d') if self.requested_last_working_day else None,
            'approved_last_working_day': self.approved_last_working_day.strftime('%Y-%m-%d') if self.approved_last_working_day else None,
            'status': self.status,
            'manager_comments': self.manager_comments,
            'hr_comments': self.hr_comments,
            'exit_interview_conducted': self.exit_interview_conducted,
            'exit_interview_feedback': self.exit_interview_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'clearances': [c.to_dict() for c in self.clearances]
        }


class ExitClearance(db.Model):
    __tablename__ = 'exit_clearances'

    id = db.Column(db.Integer, primary_key=True)
    resignation_request_id = db.Column(db.Integer, db.ForeignKey('resignation_requests.id'), nullable=False)
    department_name = db.Column(db.String(50), nullable=False)  # IT, HR, Finance, Admin, Reporting Manager
    status = db.Column(db.String(30), default='Pending')        # Pending, Cleared, Rejected
    cleared_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    cleared_at = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    dues_amount = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'resignation_request_id': self.resignation_request_id,
            'department_name': self.department_name,
            'status': self.status,
            'cleared_at': self.cleared_at.isoformat() if self.cleared_at else None,
            'remarks': self.remarks,
            'dues_amount': self.dues_amount
        }


class FnFSettlement(db.Model):
    __tablename__ = 'fnf_settlements'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    resignation_request_id = db.Column(db.Integer, db.ForeignKey('resignation_requests.id'), nullable=False)
    unpaid_salary_amount = db.Column(db.Float, default=0.0)
    leave_encashment_amount = db.Column(db.Float, default=0.0)
    gratuity_amount = db.Column(db.Float, default=0.0)
    bonus_payable = db.Column(db.Float, default=0.0)
    notice_pay_deduction = db.Column(db.Float, default=0.0)
    asset_damage_deduction = db.Column(db.Float, default=0.0)
    other_dues_deduction = db.Column(db.Float, default=0.0)
    net_settlement_amount = db.Column(db.Float, nullable=False)
    settlement_status = db.Column(db.String(30), default='Calculated')  # Calculated, Approved, Paid
    payment_date = db.Column(db.Date, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='fnf_settlements', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'resignation_request_id': self.resignation_request_id,
            'unpaid_salary_amount': self.unpaid_salary_amount,
            'leave_encashment_amount': self.leave_encashment_amount,
            'gratuity_amount': self.gratuity_amount,
            'bonus_payable': self.bonus_payable,
            'notice_pay_deduction': self.notice_pay_deduction,
            'asset_damage_deduction': self.asset_damage_deduction,
            'other_dues_deduction': self.other_dues_deduction,
            'net_settlement_amount': self.net_settlement_amount,
            'settlement_status': self.settlement_status,
            'payment_date': self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None,
            'comments': self.comments,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
