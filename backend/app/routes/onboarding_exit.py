from flask import Blueprint, request, jsonify
from app import db
from app.models.onboarding_exit import OnboardingChecklist, OnboardingTask, EmployeeDocument, ResignationRequest, ExitClearance, FnFSettlement
from app.services.onboarding_service import OnboardingService
from app.utils.auth import token_required, role_required
from datetime import datetime, date

onboarding_exit_bp = Blueprint('onboarding_exit', __name__)

@onboarding_exit_bp.route('/onboarding/checklists', methods=['GET'])
@token_required
def get_checklists(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        checklists = OnboardingChecklist.query.all()
    else:
        if not emp:
            return jsonify({'checklists': []}), 200
        checklists = OnboardingChecklist.query.filter_by(employee_id=emp.id).all()

    return jsonify({'checklists': [c.to_dict() for c in checklists]}), 200

@onboarding_exit_bp.route('/onboarding/checklists/initiate', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def initiate_onboarding(current_user):
    data = request.get_json() or {}
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'message': 'employee_id is required'}), 400

    checklist = OnboardingService.generate_default_onboarding_plan(
        employee_id=employee_id,
        hr_coordinator_id=current_user.id,
        buddy_employee_id=data.get('buddy_employee_id')
    )
    return jsonify({'message': 'Onboarding checklist created', 'checklist': checklist.to_dict()}), 201

@onboarding_exit_bp.route('/onboarding/tasks/<int:task_id>/toggle', methods=['POST'])
@token_required
def toggle_task(current_user, task_id):
    task = OnboardingTask.query.get_or_404(task_id)
    task.is_completed = not task.is_completed
    task.completed_at = datetime.utcnow() if task.is_completed else None
    db.session.commit()

    # Recalculate checklist overall status
    checklist = task.checklist
    if checklist:
        total = len(checklist.tasks)
        completed = sum(1 for t in checklist.tasks if t.is_completed)
        if completed == total and total > 0:
            checklist.overall_status = 'Completed'
            checklist.completed_at = datetime.utcnow()
        elif completed > 0:
            checklist.overall_status = 'In Progress'

    db.session.commit()
    return jsonify({'message': 'Task status updated', 'task': task.to_dict()}), 200

@onboarding_exit_bp.route('/resignations', methods=['GET'])
@token_required
def get_resignations(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        resignations = ResignationRequest.query.order_by(ResignationRequest.created_at.desc()).all()
    else:
        if not emp:
            return jsonify({'resignations': []}), 200
        resignations = ResignationRequest.query.filter_by(employee_id=emp.id).all()

    return jsonify({'resignations': [r.to_dict() for r in resignations]}), 200

@onboarding_exit_bp.route('/resignations', methods=['POST'])
@token_required
def submit_resignation(current_user):
    data = request.get_json() or {}
    if not data.get('reason') or not data.get('requested_last_working_day'):
        return jsonify({'message': 'Reason and requested_last_working_day are required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    lwd = datetime.strptime(data['requested_last_working_day'], '%Y-%m-%d').date()
    resignation = OnboardingService.initiate_resignation(emp_id, data['reason'], lwd, int(data.get('notice_period_days', 60)))
    return jsonify({'message': 'Resignation submitted successfully', 'resignation': resignation.to_dict()}), 201


@onboarding_exit_bp.route('/resignations/<int:resignation_id>/clearance', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def update_clearance(current_user, resignation_id):
    data = request.get_json() or {}
    dept_name = data.get('department_name')
    status = data.get('status', 'Cleared')

    clearance = ExitClearance.query.filter_by(resignation_request_id=resignation_id, department_name=dept_name).first()
    if not clearance:
        return jsonify({'message': 'Clearance item not found'}), 404

    clearance.status = status
    clearance.cleared_by_id = current_user.id
    clearance.cleared_at = datetime.utcnow()
    clearance.remarks = data.get('remarks')
    clearance.dues_amount = float(data.get('dues_amount', 0.0))

    db.session.commit()
    return jsonify({'message': f'Exit clearance updated for {dept_name}', 'clearance': clearance.to_dict()}), 200

@onboarding_exit_bp.route('/fnf-settlements', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_fnf_settlements(current_user):
    settlements = FnFSettlement.query.all()
    return jsonify({'settlements': [s.to_dict() for s in settlements]}), 200

@onboarding_exit_bp.route('/fnf-settlements/calculate', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def calculate_fnf(current_user):
    data = request.get_json() or {}
    resignation_id = data.get('resignation_request_id')
    if not resignation_id:
        return jsonify({'message': 'resignation_request_id is required'}), 400

    res = ResignationRequest.query.get_or_404(resignation_id)
    unpaid_sal = float(data.get('unpaid_salary_amount', 45000.0))
    leave_encash = float(data.get('leave_encashment_amount', 12000.0))
    gratuity = float(data.get('gratuity_amount', 65000.0))
    bonus = float(data.get('bonus_payable', 0.0))
    notice_ded = float(data.get('notice_pay_deduction', 0.0))
    damage_ded = float(data.get('asset_damage_deduction', 0.0))
    other_ded = float(data.get('other_dues_deduction', 0.0))

    net = (unpaid_sal + leave_encash + gratuity + bonus) - (notice_ded + damage_ded + other_ded)

    settlement = FnFSettlement.query.filter_by(resignation_request_id=resignation_id).first()
    if not settlement:
        settlement = FnFSettlement(
            employee_id=res.employee_id,
            resignation_request_id=resignation_id,
            unpaid_salary_amount=unpaid_sal,
            leave_encashment_amount=leave_encash,
            gratuity_amount=gratuity,
            bonus_payable=bonus,
            notice_pay_deduction=notice_ded,
            asset_damage_deduction=damage_ded,
            other_dues_deduction=other_ded,
            net_settlement_amount=round(net, 2),
            settlement_status='Calculated'
        )
        db.session.add(settlement)
    else:
        settlement.unpaid_salary_amount = unpaid_sal
        settlement.leave_encashment_amount = leave_encash
        settlement.gratuity_amount = gratuity
        settlement.bonus_payable = bonus
        settlement.notice_pay_deduction = notice_ded
        settlement.asset_damage_deduction = damage_ded
        settlement.other_dues_deduction = other_ded
        settlement.net_settlement_amount = round(net, 2)

    db.session.commit()
    return jsonify({'message': 'FnF settlement calculated', 'settlement': settlement.to_dict()}), 200
