from flask import Blueprint, request, jsonify
from app import db
from app.models.workforce_analytics import WorkforcePlan, AttritionRiskScore, SalaryBenchmark
from app.services.analytics_service import AnalyticsService
from app.utils.auth import token_required, role_required

workforce_bp = Blueprint('workforce', __name__)

@workforce_bp.route('/plans', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_plans(current_user):
    plans = WorkforcePlan.query.all()
    return jsonify({'plans': [p.to_dict() for p in plans]}), 200

@workforce_bp.route('/attrition-risks', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_attrition_risks(current_user):
    risks = AttritionRiskScore.query.all()
    return jsonify({'attrition_risks': [r.to_dict() for r in risks]}), 200

@workforce_bp.route('/evaluate-attrition/<int:employee_id>', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def evaluate_risk(current_user, employee_id):
    risk = AnalyticsService.evaluate_attrition_risk(employee_id)
    return jsonify({'message': 'Attrition risk evaluated', 'risk': risk.to_dict()}), 200

@workforce_bp.route('/benchmarks', methods=['GET'])
@token_required
def get_benchmarks(current_user):
    benchmarks = SalaryBenchmark.query.all()
    return jsonify({'benchmarks': [b.to_dict() for b in benchmarks]}), 200
