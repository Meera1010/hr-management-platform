from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.expense_travel import ExpenseCategory, ExpenseClaim, ExpenseItem, TravelRequest
from app.services.expense_service import ExpenseService
from app.utils.auth import token_required, role_required

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/categories', methods=['GET'])
@token_required
def get_categories(current_user):
    categories = ExpenseCategory.query.filter_by(is_active=True).all()
    return jsonify({'categories': [c.to_dict() for c in categories]}), 200

@expenses_bp.route('/claims', methods=['GET'])
@token_required
def get_claims(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        claims = ExpenseClaim.query.order_by(ExpenseClaim.created_at.desc()).all()
    else:
        if not emp:
            return jsonify({'claims': []}), 200
        claims = ExpenseClaim.query.filter_by(employee_id=emp.id).order_by(ExpenseClaim.created_at.desc()).all()

    return jsonify({'claims': [c.to_dict() for c in claims]}), 200

@expenses_bp.route('/claims', methods=['POST'])
@token_required
def submit_claim(current_user):
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    c_number = f"EXP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    claim = ExpenseClaim(
        claim_number=c_number,
        employee_id=emp_id,
        title=data['title'],
        status='Submitted'
    )
    db.session.add(claim)
    db.session.commit()

    items_data = data.get('items', [])
    for item in items_data:
        i_date = datetime.strptime(item.get('item_date', '2026-05-01'), '%Y-%m-%d').date()
        exp_item = ExpenseItem(
            claim_id=claim.id,
            category_id=item.get('category_id'),
            item_date=i_date,
            description=item.get('description'),
            amount=float(item.get('amount', 0.0))
        )
        db.session.add(exp_item)

    db.session.commit()
    ExpenseService.recalculate_claim_total(claim.id)
    return jsonify({'message': 'Expense claim submitted successfully', 'claim': claim.to_dict()}), 201


@expenses_bp.route('/claims/<int:claim_id>/approve', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def approve_claim(current_user, claim_id):
    claim = ExpenseService.approve_claim(claim_id, current_user.id)
    return jsonify({'message': 'Claim approved', 'claim': claim.to_dict()}), 200

@expenses_bp.route('/travel-requests', methods=['GET'])
@token_required
def get_travel_requests(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        requests = TravelRequest.query.order_by(TravelRequest.created_at.desc()).all()
    else:
        if not emp:
            return jsonify({'requests': []}), 200
        requests = TravelRequest.query.filter_by(employee_id=emp.id).order_by(TravelRequest.created_at.desc()).all()

    return jsonify({'requests': [r.to_dict() for r in requests]}), 200

@expenses_bp.route('/travel-requests', methods=['POST'])
@token_required
def create_travel_request(current_user):
    data = request.get_json() or {}
    if not data.get('destination') or not data.get('purpose'):
        return jsonify({'message': 'Destination and purpose are required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    s_date = datetime.strptime(data.get('departure_date', data.get('start_date', '2026-06-01')), '%Y-%m-%d').date()
    e_date = datetime.strptime(data.get('return_date', data.get('end_date', '2026-06-05')), '%Y-%m-%d').date()

    req = TravelRequest(
        request_number=f"TRV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        employee_id=emp_id,
        destination=data['destination'],
        purpose=data['purpose'],
        departure_date=s_date,
        return_date=e_date,
        estimated_cost=float(data.get('estimated_cost', 0.0)),
        status='Pending Approval'
    )
    db.session.add(req)
    db.session.commit()
    return jsonify({'message': 'Travel request created successfully', 'travel_request': req.to_dict()}), 201

