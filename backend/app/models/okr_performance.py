from datetime import datetime
from app import db

class Objective(db.Model):
    __tablename__ = 'objectives'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    level = db.Column(db.String(30), default='Individual')  # Company, Department, Team, Individual
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    owner_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    period_quarter = db.Column(db.String(10), nullable=False)  # e.g., "2026-Q1"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    progress_pct = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='On Track')  # Not Started, On Track, At Risk, Behind, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship('Employee', backref='objectives', lazy=True)
    key_results = db.relationship('KeyResult', backref='objective', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'level': self.level,
            'department_id': self.department_id,
            'owner_employee_id': self.owner_employee_id,
            'owner_name': f"{self.owner.first_name} {self.owner.last_name}" if self.owner else None,
            'period_quarter': self.period_quarter,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'progress_pct': self.progress_pct,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'key_results': [kr.to_dict() for kr in self.key_results]
        }


class KeyResult(db.Model):
    __tablename__ = 'key_results'

    id = db.Column(db.Integer, primary_key=True)
    objective_id = db.Column(db.Integer, db.ForeignKey('objectives.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(30), default='%')  # %, USD, Count, Units, Days
    weight = db.Column(db.Float, default=1.0)
    status = db.Column(db.String(30), default='On Track')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        progress = round((self.current_value / self.target_value * 100), 1) if self.target_value > 0 else 0.0
        return {
            'id': self.id,
            'objective_id': self.objective_id,
            'title': self.title,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'weight': self.weight,
            'progress_pct': min(progress, 100.0),
            'status': self.status,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ReviewCycle(db.Model):
    __tablename__ = 'review_cycles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g. "Annual Review 2026", "H1 360 Feedback"
    review_type = db.Column(db.String(30), default='360 Feedback')  # 360 Feedback, Performance Appraisal, Manager Review
    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Active')  # Scheduled, Active, Closed, Archived
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    feedbacks = db.relationship('Feedback360', backref='review_cycle', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'review_type': self.review_type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Feedback360(db.Model):
    __tablename__ = 'feedback_360'

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('review_cycles.id'), nullable=False)
    evaluatee_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    evaluator_employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    relationship = db.Column(db.String(30), default='Peer')  # Self, Peer, Manager, Direct Report
    leadership_score = db.Column(db.Float, default=0.0)      # 1 to 5
    technical_score = db.Column(db.Float, default=0.0)       # 1 to 5
    communication_score = db.Column(db.Float, default=0.0)   # 1 to 5
    teamwork_score = db.Column(db.Float, default=0.0)        # 1 to 5
    overall_rating = db.Column(db.Float, default=0.0)        # 1 to 5
    strengths = db.Column(db.Text, nullable=True)
    areas_for_improvement = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Pending')       # Pending, Submitted
    submitted_at = db.Column(db.DateTime, nullable=True)

    evaluatee = db.relationship('Employee', foreign_keys=[evaluatee_employee_id], backref='received_360_feedback', lazy=True)
    evaluator = db.relationship('Employee', foreign_keys=[evaluator_employee_id], backref='given_360_feedback', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cycle_id': self.cycle_id,
            'evaluatee_employee_id': self.evaluatee_employee_id,
            'evaluatee_name': f"{self.evaluatee.first_name} {self.evaluatee.last_name}" if self.evaluatee else None,
            'evaluator_employee_id': self.evaluator_employee_id,
            'evaluator_name': f"{self.evaluator.first_name} {self.evaluator.last_name}" if self.evaluator else None,
            'relationship': self.relationship,
            'leadership_score': self.leadership_score,
            'technical_score': self.technical_score,
            'communication_score': self.communication_score,
            'teamwork_score': self.teamwork_score,
            'overall_rating': self.overall_rating,
            'strengths': self.strengths,
            'areas_for_improvement': self.areas_for_improvement,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }


class PerformanceImprovementPlan(db.Model):
    __tablename__ = 'performance_improvement_plans'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    initiated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False, default="Performance Improvement Plan (PIP)")
    issues_identified = db.Column(db.Text, nullable=False)
    expected_outcomes = db.Column(db.Text, nullable=False)
    support_provided = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Active')  # Active, Successful, Extended, Terminated
    final_evaluation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='pips', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'title': self.title,
            'issues_identified': self.issues_identified,
            'expected_outcomes': self.expected_outcomes,
            'support_provided': self.support_provided,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'status': self.status,
            'final_evaluation': self.final_evaluation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
