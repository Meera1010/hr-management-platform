from datetime import datetime
from app import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='General')  # Technical, Soft Skills, Leadership, Compliance, Security
    level = db.Column(db.String(20), default='Beginner')    # Beginner, Intermediate, Advanced
    duration_hours = db.Column(db.Float, default=5.0)
    provider_name = db.Column(db.String(100), default='Internal Academy')
    is_mandatory = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    modules = db.relationship('CourseModule', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True)
    quizzes = db.relationship('Quiz', backref='course', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'description': self.description,
            'category': self.category,
            'level': self.level,
            'duration_hours': self.duration_hours,
            'provider_name': self.provider_name,
            'is_mandatory': self.is_mandatory,
            'is_active': self.is_active,
            'total_modules': len(self.modules),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CourseModule(db.Model):
    __tablename__ = 'course_modules'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    order_index = db.Column(db.Integer, default=1)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(30), default='Reading')  # Video, Reading, Interactive, Document
    content_url_or_text = db.Column(db.Text, nullable=True)
    estimated_minutes = db.Column(db.Integer, default=30)

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'order_index': self.order_index,
            'title': self.title,
            'content_type': self.content_type,
            'content_url_or_text': self.content_url_or_text,
            'estimated_minutes': self.estimated_minutes
        }


class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Enrolled')  # Enrolled, In Progress, Completed, Overdue
    progress_pct = db.Column(db.Float, default=0.0)
    completed_at = db.Column(db.DateTime, nullable=True)
    score_achieved = db.Column(db.Float, nullable=True)

    employee = db.relationship('Employee', backref='course_enrollments', lazy=True)
    certificates = db.relationship('Certificate', backref='enrollment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'course_category': self.course.category if self.course else None,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'status': self.status,
            'progress_pct': self.progress_pct,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'score_achieved': self.score_achieved
        }


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    passing_score_pct = db.Column(db.Float, default=70.0)
    total_marks = db.Column(db.Integer, default=100)

    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'passing_score_pct': self.passing_score_pct,
            'total_marks': self.total_marks,
            'total_questions': len(self.questions),
            'questions': [q.to_dict() for q in self.questions]
        }


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=True)
    option_d = db.Column(db.String(200), nullable=True)
    correct_option = db.Column(db.String(10), nullable=False)  # 'A', 'B', 'C', 'D'
    marks = db.Column(db.Integer, default=10)

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_option': self.correct_option,
            'marks': self.marks
        }


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('course_enrollments.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    issued_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    valid_until = db.Column(db.Date, nullable=True)
    verification_code = db.Column(db.String(50), unique=True, nullable=False)

    employee = db.relationship('Employee', backref='certificates', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'certificate_number': self.certificate_number,
            'enrollment_id': self.enrollment_id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'course_name': self.course_name,
            'issued_date': self.issued_date.strftime('%Y-%m-%d') if self.issued_date else None,
            'valid_until': self.valid_until.strftime('%Y-%m-%d') if self.valid_until else None,
            'verification_code': self.verification_code
        }


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    score_pct = db.Column(db.Float, default=0.0)
    passed = db.Column(db.Boolean, default=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'employee_id': self.employee_id,
            'score_pct': self.score_pct,
            'passed': self.passed,
            'attempted_at': self.attempted_at.isoformat() if self.attempted_at else None
        }

