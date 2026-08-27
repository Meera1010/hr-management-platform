from datetime import datetime
from app import db

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    candidate_code = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    current_role = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='Available')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('candidate_profile', uselist=False))
    
    # Relationship to Applications
    applications = db.relationship('Application', backref='candidate', lazy=True, cascade='all, delete-orphan')

    # Relationship to Resumes
    resumes = db.relationship('Resume', backref='candidate', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_code': self.candidate_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'education': self.education,
            'experience_years': self.experience_years,
            'current_role': self.current_role,
            'skills': self.skills,
            'certifications': self.certifications,
            'location': self.location,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
