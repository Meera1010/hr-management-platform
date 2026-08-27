import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.employee import Employee
from app.models.performance_review import PerformanceReview
from app.utils.auth import role_required

logger = logging.getLogger('audit')
performance_bp = Blueprint('performance', __name__)


def _get_employee_for_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return Employee.query.filter_by(user_id=user.id).first()


def _validate_score(val, name):
    try:
        score = int(val)
        if score < 1 or score > 5:
            raise ValueError
        return score, None
    except (ValueError, TypeError):
        return None, f"{name} must be an integer between 1 and 5"


# ─── LIST ──────────────────────────────────────────────────────────────────────

@performance_bp.route('', methods=['GET'])
@jwt_required()
def get_reviews():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role in ('Admin', 'HR'):
        emp_filter = request.args.get('employee_id')
        query = PerformanceReview.query
        if emp_filter:
            query = query.filter_by(employee_id=int(emp_filter))
        reviews = query.order_by(PerformanceReview.created_at.desc()).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in reviews]})

    elif role == 'Employee':
        emp = _get_employee_for_user(user_id)
        if not emp:
            return jsonify({'success': True, 'data': []})
        # Employees see only Completed reviews
        reviews = PerformanceReview.query.filter_by(
            employee_id=emp.id, status='Completed'
        ).order_by(PerformanceReview.created_at.desc()).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in reviews]})

    else:
        return jsonify({'success': False, 'message': 'Forbidden'}), 403


# ─── GET SINGLE ───────────────────────────────────────────────────────────────

@performance_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_review(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'success': False, 'message': 'Performance review not found'}), 404

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or review.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403
        if review.status != 'Completed':
            return jsonify({'success': False, 'message': 'Review not yet completed'}), 403

    return jsonify({'success': True, 'data': review.to_dict()})


# ─── CREATE (HR/Admin) ────────────────────────────────────────────────────────

@performance_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR')
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    employee_id = data.get('employee_id')
    review_period = data.get('review_period', '').strip()
    reviewer_name = data.get('reviewer_name', '').strip()
    comments = data.get('comments', '')
    status = data.get('status', 'Draft')

    if not employee_id:
        return jsonify({'success': False, 'message': 'employee_id is required'}), 400
    if not review_period:
        return jsonify({'success': False, 'message': 'review_period is required'}), 400
    if not reviewer_name:
        return jsonify({'success': False, 'message': 'reviewer_name is required'}), 400
    if status not in PerformanceReview.STATUSES:
        return jsonify({'success': False, 'message': f"status must be one of: {', '.join(PerformanceReview.STATUSES)}"}), 400

    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

    # Validate scores
    scores = {}
    for field in ['productivity_score', 'quality_score', 'teamwork_score', 'goal_score']:
        val, err = _validate_score(data.get(field), field)
        if err:
            return jsonify({'success': False, 'message': err}), 400
        scores[field] = val

    overall = PerformanceReview.compute_overall(
        scores['productivity_score'],
        scores['quality_score'],
        scores['teamwork_score'],
        scores['goal_score']
    )

    last = PerformanceReview.query.order_by(PerformanceReview.id.desc()).first()
    next_num = (last.id + 1) if last else 1
    review_code = f"PRV-{next_num:04d}"

    review = PerformanceReview(
        review_code=review_code,
        employee_id=int(employee_id),
        review_period=review_period,
        productivity_score=scores['productivity_score'],
        quality_score=scores['quality_score'],
        teamwork_score=scores['teamwork_score'],
        goal_score=scores['goal_score'],
        overall_score=overall,
        reviewer_name=reviewer_name,
        comments=comments,
        status=status
    )
    db.session.add(review)
    db.session.commit()
    logger.info(f"Audit: Performance review created. Code: {review_code}, Employee ID: {employee_id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Performance review created', 'data': review.to_dict()}), 201


# ─── UPDATE (HR/Admin) ────────────────────────────────────────────────────────

@performance_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('Admin', 'HR')
def update_review(id):
    user_id = get_jwt_identity()
    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'success': False, 'message': 'Performance review not found'}), 404

    data = request.get_json() or {}

    if 'review_period' in data:
        review.review_period = data['review_period'].strip()
    if 'reviewer_name' in data:
        review.reviewer_name = data['reviewer_name'].strip()
    if 'comments' in data:
        review.comments = data['comments']
    if 'status' in data:
        if data['status'] not in PerformanceReview.STATUSES:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        review.status = data['status']

    for field in ['productivity_score', 'quality_score', 'teamwork_score', 'goal_score']:
        if field in data:
            val, err = _validate_score(data[field], field)
            if err:
                return jsonify({'success': False, 'message': err}), 400
            setattr(review, field, val)

    review.recalculate_overall()
    db.session.commit()
    logger.info(f"Audit: Performance review updated. ID: {id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Performance review updated', 'data': review.to_dict()})


# ─── DELETE (HR/Admin) ────────────────────────────────────────────────────────

@performance_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin', 'HR')
def delete_review(id):
    user_id = get_jwt_identity()
    review = PerformanceReview.query.get(id)
    if not review:
        return jsonify({'success': False, 'message': 'Performance review not found'}), 404

    db.session.delete(review)
    db.session.commit()
    logger.info(f"Audit: Performance review deleted. ID: {id}, By User: {user_id}")
    return jsonify({'success': True, 'message': 'Performance review deleted'})


# ─── EMPLOYEE PERFORMANCE ─────────────────────────────────────────────────────

@performance_bp.route('/employee/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_performance(employee_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    role = user.role.name if user and user.role else ''

    if role not in ('Admin', 'HR'):
        emp = _get_employee_for_user(user_id)
        if not emp or emp.id != employee_id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403
        reviews = PerformanceReview.query.filter_by(
            employee_id=employee_id, status='Completed'
        ).order_by(PerformanceReview.created_at.desc()).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in reviews]})

    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify({'success': False, 'message': 'Employee not found'}), 404

    reviews = PerformanceReview.query.filter_by(employee_id=employee_id).order_by(PerformanceReview.created_at.desc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in reviews]})
