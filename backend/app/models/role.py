from datetime import datetime
from app import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to User
    users = db.relationship('User', back_populates='role')

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Role):
            return self.id == other.id
        return super().__eq__(other)

    def __str__(self):
        return self.name or ''

    def __repr__(self):
        return f"<Role {self.name}>"

    def __hash__(self):
        return hash(self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
