from datetime import datetime
from app import db


class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'

    STATUSES = ['Draft', 'Completed']

    id = db.Column(db.Integer, primary_key=True)
    review_code = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    review_period = db.Column(db.String(100), nullable=False)  # e.g. "Q1 2026", "Annual 2026"
    productivity_score = db.Column(db.Integer, nullable=False)  # 1–5
    quality_score = db.Column(db.Integer, nullable=False)       # 1–5
    teamwork_score = db.Column(db.Integer, nullable=False)      # 1–5
    goal_score = db.Column(db.Integer, nullable=False)          # 1–5
    overall_score = db.Column(db.Float, nullable=False)         # Calculated: average of 4 scores
    reviewer_name = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Draft')
    # Status: Draft, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('Employee', backref=db.backref('performance_reviews', lazy=True, cascade='all, delete-orphan'))

    @staticmethod
    def compute_overall(productivity, quality, teamwork, goal):
        """Compute overall score as average of four dimensions (rounded to 2dp)."""
        return round((productivity + quality + teamwork + goal) / 4.0, 2)

    def recalculate_overall(self):
        self.overall_score = self.compute_overall(
            self.productivity_score,
            self.quality_score,
            self.teamwork_score,
            self.goal_score
        )

    def to_dict(self):
        return {
            'id': self.id,
            'review_code': self.review_code,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_code': self.employee.employee_code if self.employee else None,
            'department_name': self.employee.department.name if self.employee and self.employee.department else None,
            'review_period': self.review_period,
            'productivity_score': self.productivity_score,
            'quality_score': self.quality_score,
            'teamwork_score': self.teamwork_score,
            'goal_score': self.goal_score,
            'overall_score': self.overall_score,
            'reviewer_name': self.reviewer_name,
            'comments': self.comments,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
