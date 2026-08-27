from app import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    application_code = db.Column(db.String(50), unique=True, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Submitted') # Submitted, Under Review, Shortlisted, Rejected, Withdrawn, Selected
    recruiter_notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraint to prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint('candidate_id', 'job_id', name='uq_candidate_job'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'application_code': self.application_code,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'cover_letter': self.cover_letter,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'status': self.status,
            'recruiter_notes': self.recruiter_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            # Eagerly access related info if needed or leave for route expansion
            'candidate_name': f"{self.candidate.first_name} {self.candidate.last_name}" if self.candidate else None,
            'job_title': self.job.title if self.job else None,
            'department_name': self.job.department.name if self.job and self.job.department else None
        }
