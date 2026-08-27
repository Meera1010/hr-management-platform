from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.learning import Course, CourseModule, CourseEnrollment, Quiz, QuizQuestion, Certificate, QuizAttempt
from app.services.learning_service import LearningService
from app.utils.auth import token_required, role_required

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    courses = Course.query.filter_by(is_active=True).all()
    return jsonify({'courses': [c.to_dict() for c in courses]}), 200

@learning_bp.route('/courses', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_course(current_user):
    data = request.get_json() or {}
    if not data.get('title') or not data.get('code'):
        return jsonify({'message': 'Title and code are required'}), 400

    course = Course(
        title=data['title'],
        code=data['code'],
        description=data.get('description'),
        category=data.get('category', 'General'),
        level=data.get('level', 'Beginner'),
        duration_hours=float(data.get('duration_hours', 5.0)),
        provider_name=data.get('provider_name', 'Internal Academy'),
        is_mandatory=bool(data.get('is_mandatory', False))
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully', 'course': course.to_dict()}), 201

@learning_bp.route('/enrollments', methods=['GET'])
@token_required
def get_enrollments(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        enrollments = CourseEnrollment.query.all()
    else:
        if not emp:
            return jsonify({'enrollments': []}), 200
        enrollments = CourseEnrollment.query.filter_by(employee_id=emp.id).all()

    return jsonify({'enrollments': [e.to_dict() for e in enrollments]}), 200

@learning_bp.route('/enrollments', methods=['POST'])
@token_required
def enroll_course(current_user):
    data = request.get_json() or {}
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({'message': 'course_id is required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    existing = CourseEnrollment.query.filter_by(course_id=course_id, employee_id=emp_id).first()
    if existing:
        return jsonify({'message': 'Already enrolled', 'enrollment': existing.to_dict()}), 200

    enrollment = CourseEnrollment(
        course_id=course_id,
        employee_id=emp_id,
        status='Enrolled',
        progress_pct=0.0
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrolled successfully', 'enrollment': enrollment.to_dict()}), 201

@learning_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json() or {}
    answers = data.get('answers', {})
    enrollment_id = data.get('enrollment_id')

    if not enrollment_id:
        return jsonify({'message': 'enrollment_id is required'}), 400

    result = LearningService.grade_quiz(quiz_id, enrollment_id, answers)
    return jsonify({'message': 'Quiz graded', 'result': result}), 200

@learning_bp.route('/certificates', methods=['GET'])
@token_required
def get_certificates(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        certificates = Certificate.query.all()
    else:
        if not emp:
            return jsonify({'certificates': []}), 200
        certificates = Certificate.query.filter_by(employee_id=emp.id).all()

    return jsonify({'certificates': [c.to_dict() for c in certificates]}), 200
