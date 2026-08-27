from datetime import datetime
from app import db

class InterviewFeedback(db.Model):
    __tablename__ = 'interview_feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False, unique=True)
    technical_score = db.Column(db.Integer, nullable=False) # 1-5
    communication_score = db.Column(db.Integer, nullable=False) # 1-5
    problem_solving_score = db.Column(db.Integer, nullable=False) # 1-5
    overall_score = db.Column(db.Float, nullable=False) # Average (1.00 - 5.00)
    recommendation = db.Column(db.String(50), nullable=False) # Strongly Recommend, Recommend, Neutral, Do Not Recommend
    comments = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_overall_score(self):
        return round((self.technical_score + self.communication_score + self.problem_solving_score) / 3.0, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'technical_score': self.technical_score,
            'communication_score': self.communication_score,
            'problem_solving_score': self.problem_solving_score,
            'overall_score': self.overall_score,
            'recommendation': self.recommendation,
            'comments': self.comments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
