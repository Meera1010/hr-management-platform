from flask import Blueprint, request, jsonify
from app import db
from app.models.training import TrainingCourse, TrainingAssignment
from app.models.employee import Employee
from app.models.notification import Notification
from app.utils.auth import token_required, role_required
from datetime import datetime

training_bp = Blueprint('training', __name__, url_prefix='/api/training')

@training_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    """List training courses with status and keyword filter"""
    status = request.args.get('status')
    query = request.args.get('query')

    q = TrainingCourse.query
    if status:
        q = q.filter_by(status=status)
    if query:
        q = q.filter(TrainingCourse.title.ilike(f"%{query}%") | TrainingCourse.category.ilike(f"%{query}%"))

    courses = q.order_by(TrainingCourse.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(courses),
        'data': [c.to_dict() for c in courses]
    }), 200

@training_bp.route('/courses/<int:course_id>', methods=['GET'])
@token_required
def get_course_detail(current_user, course_id):
    course = TrainingCourse.query.get_or_404(course_id)
    return jsonify({'success': True, 'data': course.to_dict()}), 200

@training_bp.route('/courses', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_course(current_user):
    data = request.get_json() or {}
    if not data.get('title') or not data.get('category'):
        return jsonify({'success': False, 'message': 'Title and Category are required.'}), 400

    course_count = TrainingCourse.query.count() + 1
    code = f"TRN-{course_count:04d}"

    course = TrainingCourse(
        course_code=data.get('course_code') or code,
        title=data.get('title'),
        category=data.get('category'),
        description=data.get('description'),
        duration_hours=int(data.get('duration_hours', 1)),
        instructor=data.get('instructor'),
        status=data.get('status', 'Active')
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Training course created successfully.', 'data': course.to_dict()}), 201

@training_bp.route('/courses/<int:course_id>', methods=['PUT'])
@token_required
@role_required(['Admin', 'HR'])
def update_course(current_user, course_id):
    course = TrainingCourse.query.get_or_404(course_id)
    data = request.get_json() or {}

    if 'title' in data: course.title = data['title']
    if 'category' in data: course.category = data['category']
    if 'description' in data: course.description = data['description']
    if 'duration_hours' in data: course.duration_hours = int(data['duration_hours'])
    if 'instructor' in data: course.instructor = data['instructor']
    if 'status' in data: course.status = data['status']

    db.session.commit()
    return jsonify({'success': True, 'message': 'Course updated successfully.', 'data': course.to_dict()}), 200

@training_bp.route('/assignments', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def assign_training(current_user):
    data = request.get_json() or {}
    course_id = data.get('course_id')
    employee_id = data.get('employee_id')

    if not course_id or not employee_id:
        return jsonify({'success': False, 'message': 'course_id and employee_id are required.'}), 400

    course = TrainingCourse.query.get_or_404(course_id)
    employee = Employee.query.get_or_404(employee_id)

    assign_count = TrainingAssignment.query.count() + 1
    assignment_code = f"TAS-{assign_count:04d}"

    assignment = TrainingAssignment(
        assignment_code=assignment_code,
        course_id=course.id,
        employee_id=employee.id,
        status='Assigned',
        assigned_date=data.get('assigned_date') or datetime.now().strftime('%Y-%m-%d'),
        due_date=data.get('due_date')
    )
    db.session.add(assignment)
    db.session.commit()

    # Send notification to assigned employee
    if employee.user_id:
        Notification.create_notification(
            user_id=employee.user_id,
            title='New Training Assigned',
            message=f'You have been assigned to training course "{course.title}". Due date: {data.get("due_date") or "N/A"}.',
            link='/employee/training',
            type='info'
        )

    return jsonify({'success': True, 'message': 'Training assigned successfully.', 'data': assignment.to_dict()}), 201

@training_bp.route('/my-trainings', methods=['GET'])
@token_required
def get_my_trainings(current_user):
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    if not employee:
        return jsonify({'success': True, 'data': []}), 200

    assignments = TrainingAssignment.query.filter_by(employee_id=employee.id).order_by(TrainingAssignment.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(assignments),
        'data': [a.to_dict() for a in assignments]
    }), 200

@training_bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@token_required
def update_assignment(current_user, assignment_id):
    assignment = TrainingAssignment.query.get_or_404(assignment_id)
    data = request.get_json() or {}

    # Check access: Admin/HR or assigned Employee
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    is_owner = employee and employee.id == assignment.employee_id
    is_admin_hr = current_user.role in ['Admin', 'HR']

    if not (is_owner or is_admin_hr):
        return jsonify({'success': False, 'message': 'Unauthorized to update this assignment.'}), 403

    if 'status' in data:
        assignment.status = data['status']
        if data['status'] == 'Completed' and not assignment.completion_date:
            assignment.completion_date = datetime.now().strftime('%Y-%m-%d')

    if 'score' in data: assignment.score = float(data['score'])
    if 'feedback' in data: assignment.feedback = data['feedback']

    db.session.commit()
    return jsonify({'success': True, 'message': 'Assignment updated.', 'data': assignment.to_dict()}), 200

@training_bp.route('/assignments', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_all_assignments(current_user):
    assignments = TrainingAssignment.query.order_by(TrainingAssignment.created_at.desc()).all()
    return jsonify({
        'success': True,
        'count': len(assignments),
        'data': [a.to_dict() for a in assignments]
    }), 200
