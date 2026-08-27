from app import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_code = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text, nullable=True)
    required_skills = db.Column(db.Text, nullable=True)
    preferred_skills = db.Column(db.Text, nullable=True)
    experience_required = db.Column(db.String(100), nullable=True)
    education_required = db.Column(db.String(150), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    employment_type = db.Column(db.String(50), nullable=True) # Full Time, Part Time, Contract, Internship
    salary_range = db.Column(db.String(100), nullable=True)
    application_deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='Draft') # Draft, Open, Closed, Archived
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship('Department', backref=db.backref('jobs', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_jobs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'job_code': self.job_code,
            'title': self.title,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'description': self.description,
            'responsibilities': self.responsibilities,
            'required_skills': self.required_skills,
            'preferred_skills': self.preferred_skills,
            'experience_required': self.experience_required,
            'education_required': self.education_required,
            'location': self.location,
            'employment_type': self.employment_type,
            'salary_range': self.salary_range,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
