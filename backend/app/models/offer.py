from datetime import datetime
from app import db

class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    offer_code = db.Column(db.String(50), unique=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False, default='Full Time')
    offered_salary = db.Column(db.String(100), nullable=False) # Demo salary e.g. "$85,000 / year"
    start_date = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    expiration_date = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    status = db.Column(db.String(50), default='Draft') # Draft, Sent, Accepted, Declined, Expired, Cancelled
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    application = db.relationship('Application', backref=db.backref('offers', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'offer_code': self.offer_code,
            'application_id': self.application_id,
            'candidate_id': self.application.candidate_id if self.application else None,
            'candidate_name': f"{self.application.candidate.first_name} {self.application.candidate.last_name}" if self.application and self.application.candidate else None,
            'candidate_email': self.application.candidate.email if self.application and self.application.candidate else None,
            'job_id': self.application.job_id if self.application else None,
            'job_title': self.job_title,
            'employment_type': self.employment_type,
            'offered_salary': self.offered_salary,
            'start_date': self.start_date,
            'expiration_date': self.expiration_date,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
