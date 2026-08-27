from flask import Blueprint, request, jsonify
from app import db
from app.models.okr_performance import Objective, KeyResult, ReviewCycle, Feedback360, PerformanceImprovementPlan
from app.services.okr_service import OkrService
from app.utils.auth import token_required, role_required
from datetime import datetime, date

okrs_bp = Blueprint('okrs', __name__)

@okrs_bp.route('/objectives', methods=['GET'])
@token_required
def get_objectives(current_user):
    period = request.args.get('period_quarter')
    level = request.args.get('level')
    query = Objective.query

    if period:
        query = query.filter_by(period_quarter=period)
    if level:
        query = query.filter_by(level=level)

    objectives = query.order_by(Objective.created_at.desc()).all()
    return jsonify({'objectives': [o.to_dict() for o in objectives]}), 200

@okrs_bp.route('/objectives', methods=['POST'])
@token_required
def create_objective(current_user):
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('owner_employee_id') if current_user.role in ['Admin', 'HR'] and data.get('owner_employee_id') else (emp.id if emp else current_user.id)

    s_date = datetime.strptime(data.get('start_date', '2026-01-01'), '%Y-%m-%d').date()
    e_date = datetime.strptime(data.get('end_date', '2026-03-31'), '%Y-%m-%d').date()

    obj = Objective(
        title=data['title'],
        description=data.get('description'),
        period_quarter=data.get('period_quarter', '2026-Q1'),
        level=data.get('level', 'Individual'),
        department_id=data.get('department_id'),
        owner_employee_id=emp_id,
        start_date=s_date,
        end_date=e_date,
        status='On Track'
    )
    db.session.add(obj)
    db.session.commit()
    return jsonify({'message': 'Objective created successfully', 'objective': obj.to_dict()}), 201


@okrs_bp.route('/objectives/<int:objective_id>/key-results', methods=['POST'])
@token_required
def add_key_result(current_user, objective_id):
    data = request.get_json() or {}
    if not data.get('title') or 'target_value' not in data:
        return jsonify({'message': 'Title and target_value are required'}), 400

    kr = KeyResult(
        objective_id=objective_id,
        title=data['title'],
        target_value=float(data['target_value']),
        current_value=float(data.get('current_value', 0.0)),
        unit=data.get('unit', '%'),
        weight=float(data.get('weight', 1.0))
    )
    db.session.add(kr)
    db.session.commit()

    OkrService.recalculate_objective_progress(objective_id)
    return jsonify({'message': 'Key result added', 'key_result': kr.to_dict()}), 201

@okrs_bp.route('/key-results/<int:kr_id>/update-progress', methods=['POST'])
@token_required
def update_kr_progress(current_user, kr_id):
    kr = KeyResult.query.get_or_404(kr_id)
    data = request.get_json() or {}
    new_val = data.get('current_value')
    if new_val is None:
        return jsonify({'message': 'current_value is required'}), 400

    kr.current_value = float(new_val)
    db.session.commit()

    OkrService.recalculate_objective_progress(kr.objective_id)
    return jsonify({'message': 'Progress updated', 'key_result': kr.to_dict()}), 200

@okrs_bp.route('/review-cycles', methods=['GET'])
@token_required
def get_review_cycles(current_user):
    cycles = ReviewCycle.query.order_by(ReviewCycle.created_at.desc()).all()
    return jsonify({'cycles': [c.to_dict() for c in cycles]}), 200

@okrs_bp.route('/feedback-360', methods=['GET'])
@okrs_bp.route('/360-feedback', methods=['GET'])
@token_required
def get_feedback_360(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        feedbacks = Feedback360.query.all()
    else:
        if not emp:
            return jsonify({'feedbacks': []}), 200
        feedbacks = Feedback360.query.filter_by(reviewee_employee_id=emp.id).all()

    return jsonify({'feedbacks': [f.to_dict() for f in feedbacks]}), 200

@okrs_bp.route('/pips', methods=['GET'])
@token_required
def get_pips(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        pips = PerformanceImprovementPlan.query.all()
    else:
        if not emp:
            return jsonify({'pips': []}), 200
        pips = PerformanceImprovementPlan.query.filter_by(employee_id=emp.id).all()

    return jsonify({'pips': [p.to_dict() for p in pips]}), 200
