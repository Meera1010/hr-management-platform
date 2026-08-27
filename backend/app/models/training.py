from app import db
from datetime import datetime

class TrainingCourse(db.Model):
    __tablename__ = 'training_courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False) # e.g. Technical, Compliance, Leadership, HR
    description = db.Column(db.Text, nullable=True)
    duration_hours = db.Column(db.Integer, default=1)
    instructor = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='Active') # Active, Inactive, Archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('TrainingAssignment', backref='course', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'duration_hours': self.duration_hours,
            'instructor': self.instructor,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'assignments_count': len(self.assignments)
        }

class TrainingAssignment(db.Model):
    __tablename__ = 'training_assignments'

    id = db.Column(db.Integer, primary_key=True)
    assignment_code = db.Column(db.String(20), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('training_courses.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    status = db.Column(db.String(30), default='Assigned') # Assigned, In Progress, Completed, Overdue
    assigned_date = db.Column(db.String(10), nullable=False) # YYYY-MM-DD
    due_date = db.Column(db.String(10), nullable=True) # YYYY-MM-DD
    completion_date = db.Column(db.String(10), nullable=True) # YYYY-MM-DD
    score = db.Column(db.Float, nullable=True) # Optional test score percentage
    feedback = db.Column(db.Text, nullable=True)
    employee = db.relationship('Employee', backref='training_assignments', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'assignment_code': self.assignment_code,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'course_code': self.course.course_code if self.course else None,
            'course_category': self.course.category if self.course else None,
            'duration_hours': self.course.duration_hours if self.course else 1,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_code': self.employee.employee_code if self.employee else None,
            'department_name': self.employee.department.name if (self.employee and self.employee.department) else None,
            'status': self.status,
            'assigned_date': self.assigned_date,
            'due_date': self.due_date,
            'completion_date': self.completion_date,
            'score': self.score,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
