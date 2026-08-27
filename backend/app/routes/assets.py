from flask import Blueprint, request, jsonify
from app import db
from app.models.assets import AssetCategory, Asset, AssetAssignment, AssetMaintenance, SoftwareLicense, ITTicket
from app.services.asset_service import AssetService
from app.utils.auth import token_required, role_required
from datetime import datetime, date

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/categories', methods=['GET'])
@token_required
def get_categories(current_user):
    categories = AssetCategory.query.all()
    return jsonify({'categories': [c.to_dict() for c in categories]}), 200

@assets_bp.route('/categories', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_category(current_user):
    data = request.get_json() or {}
    if not data.get('name') or not data.get('code'):
        return jsonify({'message': 'Name and Code are required'}), 400

    category = AssetCategory(
        name=data['name'],
        code=data['code'],
        description=data.get('description')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created', 'category': category.to_dict()}), 201

@assets_bp.route('/', methods=['GET'])
@token_required
def get_assets(current_user):
    category_id = request.args.get('category_id')
    status = request.args.get('status')
    query = Asset.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if status:
        query = query.filter_by(status=status)

    assets = query.all()
    return jsonify({'assets': [a.to_dict() for a in assets]}), 200

@assets_bp.route('/', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_asset(current_user):
    data = request.get_json() or {}
    if not data.get('asset_tag') or not data.get('name') or not data.get('category_id'):
        return jsonify({'message': 'Asset tag, name, and category_id are required'}), 400

    p_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data.get('purchase_date') else None
    w_date = datetime.strptime(data['warranty_expiry_date'], '%Y-%m-%d').date() if data.get('warranty_expiry_date') else None

    asset = Asset(
        asset_tag=data['asset_tag'],
        name=data['name'],
        category_id=data['category_id'],
        serial_number=data.get('serial_number'),
        model_name=data.get('model_name'),
        manufacturer=data.get('manufacturer'),
        purchase_date=p_date,
        purchase_cost=float(data.get('purchase_cost', 0.0)),
        warranty_expiry_date=w_date,
        status=data.get('status', 'Available'),
        condition=data.get('condition', 'Excellent'),
        location=data.get('location', 'Headquarters'),
        vendor_name=data.get('vendor_name'),
        notes=data.get('notes')
    )
    db.session.add(asset)
    db.session.commit()
    return jsonify({'message': 'Asset created successfully', 'asset': asset.to_dict()}), 201

@assets_bp.route('/<int:asset_id>/assign', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def assign_asset(current_user, asset_id):
    data = request.get_json() or {}
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'message': 'employee_id is required'}), 400

    try:
        assignment = AssetService.assign_asset_to_employee(asset_id, employee_id, current_user.id, data.get('notes'))
        return jsonify({'message': 'Asset assigned', 'assignment': assignment.to_dict()}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@assets_bp.route('/<int:asset_id>/return', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def return_asset(current_user, asset_id):
    data = request.get_json() or {}
    condition = data.get('condition', 'Good')
    notes = data.get('notes')

    asset = AssetService.return_asset(asset_id, condition, notes)
    return jsonify({'message': 'Asset returned successfully', 'asset': asset.to_dict()}), 200

@assets_bp.route('/my-assets', methods=['GET'])
@token_required
def get_my_assets(current_user):
    emp = getattr(current_user, 'employee', None)
    if not emp:
        return jsonify({'assignments': []}), 200

    assignments = AssetAssignment.query.filter_by(employee_id=emp.id, status='Active').all()
    return jsonify({'assignments': [a.to_dict() for a in assignments]}), 200

@assets_bp.route('/tickets', methods=['GET'])
@token_required
def get_it_tickets(current_user):
    emp = getattr(current_user, 'employee', None)
    if current_user.role in ['Admin', 'HR']:
        tickets = ITTicket.query.order_by(ITTicket.created_at.desc()).all()
    else:
        if not emp:
            return jsonify({'tickets': []}), 200
        tickets = ITTicket.query.filter_by(employee_id=emp.id).order_by(ITTicket.created_at.desc()).all()

    return jsonify({'tickets': [t.to_dict() for t in tickets]}), 200

@assets_bp.route('/tickets', methods=['POST'])
@token_required
def create_it_ticket(current_user):
    data = request.get_json() or {}
    if not data.get('subject') or not data.get('description'):
        return jsonify({'message': 'Subject and description are required'}), 400

    emp = getattr(current_user, 'employee', None)
    emp_id = data.get('employee_id') if current_user.role in ['Admin', 'HR'] and data.get('employee_id') else (emp.id if emp else current_user.id)

    ticket = ITTicket(
        ticket_number=f"TICK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        employee_id=emp_id,
        asset_id=data.get('asset_id'),
        category=data.get('category', 'Hardware'),
        subject=data['subject'],
        description=data['description'],
        priority=data.get('priority', 'Medium'),
        status='Open'
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'IT ticket submitted', 'ticket': ticket.to_dict()}), 201

