import json
from datetime import datetime
from app import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    resume_code = db.Column(db.String(50), unique=True, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # PDF, TXT, DOCX
    file_size = db.Column(db.Integer, nullable=False)     # size in bytes
    extracted_text = db.Column(db.Text, nullable=True)
    extracted_skills = db.Column(db.Text, nullable=True)  # JSON formatted list of skills
    status = db.Column(db.String(50), default='Uploaded') # Uploaded, Parsed, Active, Archived
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_skills_list(self):
        if not self.extracted_skills:
            return []
        try:
            return json.loads(self.extracted_skills)
        except Exception:
            return []

    def set_skills_list(self, skills_list):
        if isinstance(skills_list, list):
            self.extracted_skills = json.dumps(skills_list)
        else:
            self.extracted_skills = json.dumps([])

    def to_dict(self):
        return {
            'id': self.id,
            'resume_code': self.resume_code,
            'candidate_id': self.candidate_id,
            'candidate_name': f"{self.candidate.first_name} {self.candidate.last_name}" if self.candidate else None,
            'filename': self.filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'extracted_text': self.extracted_text,
            'extracted_skills': self.get_skills_list(),
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
