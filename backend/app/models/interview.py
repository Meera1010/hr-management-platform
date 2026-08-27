from datetime import datetime
from app import db

class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    interview_code = db.Column(db.String(50), unique=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    interviewer_name = db.Column(db.String(100), nullable=False)
    interview_type = db.Column(db.String(50), nullable=False, default='Technical') # Technical, HR, Managerial, General
    scheduled_date = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    scheduled_time = db.Column(db.String(20), nullable=False) # HH:MM
    duration_minutes = db.Column(db.Integer, nullable=False, default=45) # 30, 45, 60, 90
    meeting_link = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='Scheduled') # Scheduled, Completed, Cancelled, Rescheduled
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    application = db.relationship('Application', backref=db.backref('interviews', lazy=True, cascade='all, delete-orphan'))
    feedback = db.relationship('InterviewFeedback', backref='interview', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'interview_code': self.interview_code,
            'application_id': self.application_id,
            'application_code': self.application.application_code if self.application else None,
            'candidate_id': self.application.candidate_id if self.application else None,
            'candidate_name': f"{self.application.candidate.first_name} {self.application.candidate.last_name}" if self.application and self.application.candidate else None,
            'candidate_email': self.application.candidate.email if self.application and self.application.candidate else None,
            'job_id': self.application.job_id if self.application else None,
            'job_title': self.application.job.title if self.application and self.application.job else None,
            'job_code': self.application.job.job_code if self.application and self.application.job else None,
            'interviewer_name': self.interviewer_name,
            'interview_type': self.interview_type,
            'scheduled_date': self.scheduled_date,
            'scheduled_time': self.scheduled_time,
            'duration_minutes': self.duration_minutes,
            'meeting_link': self.meeting_link,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'has_feedback': self.feedback is not None,
            'feedback': self.feedback.to_dict() if self.feedback else None
        }

