from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models.compliance_audit import GrievanceTicket, CompanyPolicy, PolicyAcknowledgment, AuditLog
from app.services.compliance_service import ComplianceService
from app.utils.auth import token_required, role_required

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/grievances', methods=['GET'])
@token_required
def get_grievances(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        tickets = GrievanceTicket.query.order_by(GrievanceTicket.created_at.desc()).all()
    else:
        if not emp:
            return jsonify({'grievances': []}), 200
        tickets = GrievanceTicket.query.filter_by(raised_by_employee_id=emp.id).order_by(GrievanceTicket.created_at.desc()).all()

    return jsonify({'grievances': [t.to_dict() for t in tickets]}), 200

@compliance_bp.route('/grievances', methods=['POST'])
@token_required
def submit_grievance(current_user):
    data = request.get_json() or {}
    if not data.get('subject') or not data.get('description'):
        return jsonify({'message': 'Subject and description are required'}), 400

    is_anon = bool(data.get('is_anonymous', False))
    emp = getattr(current_user, 'employee', None)
    emp_id = None if is_anon else (emp.id if emp else current_user.id)

    t_number = f"GRIEV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    ticket = GrievanceTicket(
        ticket_number=t_number,
        raised_by_employee_id=emp_id,
        category=data.get('category', 'General'),
        subject=data['subject'],
        description=data['description'],
        is_anonymous=is_anon,
        status='Open'
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'Grievance submitted successfully', 'ticket': ticket.to_dict(), 'grievance': ticket.to_dict()}), 201



@compliance_bp.route('/policies', methods=['GET'])
@token_required
def get_policies(current_user):
    policies = CompanyPolicy.query.filter_by(is_active=True).all()
    return jsonify({'policies': [p.to_dict() for p in policies]}), 200

@compliance_bp.route('/policies/<int:policy_id>/acknowledge', methods=['POST'])
@token_required
def acknowledge_policy(current_user, policy_id):
    emp = getattr(current_user, 'employee', None)
    emp_id = emp.id if emp else current_user.id

    ack = ComplianceService.acknowledge_policy(emp_id, policy_id)
    return jsonify({'message': 'Policy acknowledged', 'acknowledgment': ack.to_dict()}), 200

@compliance_bp.route('/audit-logs', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_audit_logs(current_user):
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return jsonify({'logs': [l.to_dict() for l in logs]}), 200

