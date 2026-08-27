import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.candidate import Candidate
from app.models.application import Application
from app.models.offer import Offer
from app.utils.auth import role_required

logger = logging.getLogger('audit')
offers_bp = Blueprint('offers', __name__)

@offers_bp.route('', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_offers():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate:
            return jsonify({"success": True, "data": []})

        apps = Application.query.filter_by(candidate_id=candidate.id).all()
        app_ids = [a.id for a in apps]
        offers = Offer.query.filter(Offer.application_id.in_(app_ids)).order_by(Offer.created_at.desc()).all()
        return jsonify({"success": True, "data": [o.to_dict() for o in offers]})

    else:
        offers = Offer.query.order_by(Offer.created_at.desc()).all()
        return jsonify({"success": True, "data": [o.to_dict() for o in offers]})


@offers_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_offer(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    offer = Offer.query.get(id)

    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or offer.application.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to view this offer"}), 403

    return jsonify({"success": True, "data": offer.to_dict()})


@offers_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR')
def create_offer():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    application_id = data.get('application_id')
    job_title = data.get('job_title')
    employment_type = data.get('employment_type', 'Full Time')
    offered_salary = data.get('offered_salary')
    start_date = data.get('start_date')
    expiration_date = data.get('expiration_date')
    notes = data.get('notes', '')

    if not application_id or not job_title or not offered_salary or not start_date or not expiration_date:
        return jsonify({"success": False, "message": "application_id, job_title, offered_salary, start_date, and expiration_date are required"}), 400

    application = Application.query.get(application_id)
    if not application:
        return jsonify({"success": False, "message": "Application not found"}), 404

    # Date Validation
    if expiration_date < start_date:
        return jsonify({"success": False, "message": "Expiration date cannot be earlier than start date"}), 400

    last_off = Offer.query.order_by(Offer.id.desc()).first()
    next_num = (last_off.id + 1) if last_off else 1
    offer_code = f"OFF-{next_num:04d}"

    offer = Offer(
        offer_code=offer_code,
        application_id=application_id,
        job_title=job_title,
        employment_type=employment_type,
        offered_salary=offered_salary,
        start_date=start_date,
        expiration_date=expiration_date,
        status=data.get('status', 'Draft'),
        notes=notes
    )

    db.session.add(offer)
    db.session.commit()

    logger.info(f"Audit: Offer created. Code: {offer.offer_code}, Application ID: {application_id}, Created By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Offer created successfully",
        "data": offer.to_dict()
    }), 201


@offers_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('Admin', 'HR')
def update_offer(id):
    user_id = get_jwt_identity()
    offer = Offer.query.get(id)
    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    data = request.get_json() or {}

    start_date = data.get('start_date', offer.start_date)
    expiration_date = data.get('expiration_date', offer.expiration_date)

    if expiration_date < start_date:
        return jsonify({"success": False, "message": "Expiration date cannot be earlier than start date"}), 400

    offer.job_title = data.get('job_title', offer.job_title)
    offer.employment_type = data.get('employment_type', offer.employment_type)
    offer.offered_salary = data.get('offered_salary', offer.offered_salary)
    offer.start_date = start_date
    offer.expiration_date = expiration_date
    offer.notes = data.get('notes', offer.notes)
    if 'status' in data:
        offer.status = data['status']

    db.session.commit()

    logger.info(f"Audit: Offer updated. ID: {id}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Offer updated successfully",
        "data": offer.to_dict()
    })


@offers_bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
@role_required('Admin', 'HR')
def update_offer_status(id):
    user_id = get_jwt_identity()
    offer = Offer.query.get(id)
    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    data = request.get_json() or {}
    new_status = data.get('status')
    valid_statuses = ['Draft', 'Sent', 'Accepted', 'Declined', 'Expired', 'Cancelled']

    if not new_status or new_status not in valid_statuses:
        return jsonify({"success": False, "message": "Invalid offer status"}), 400

    old_status = offer.status
    offer.status = new_status
    db.session.commit()

    logger.info(f"Audit: Offer status changed. ID: {id}, Old: {old_status}, New: {new_status}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Offer status updated successfully",
        "data": offer.to_dict()
    })


@offers_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin', 'HR')
def delete_offer(id):
    user_id = get_jwt_identity()
    offer = Offer.query.get(id)
    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    db.session.delete(offer)
    db.session.commit()

    logger.info(f"Audit: Offer deleted. ID: {id}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Offer deleted successfully"
    })


@offers_bp.route('/<int:id>/accept', methods=['POST'])
@jwt_required()
@role_required('Candidate')
def accept_offer(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    candidate = Candidate.query.filter_by(user_id=user.id).first()

    offer = Offer.query.get(id)
    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    if not candidate or offer.application.candidate_id != candidate.id:
        return jsonify({"success": False, "message": "You do not have permission to accept this offer"}), 403

    if offer.status != 'Sent':
        return jsonify({"success": False, "message": f"Offer cannot be accepted from current status '{offer.status}'"}), 400

    offer.status = 'Accepted'
    if offer.application:
        offer.application.status = 'Selected'

    db.session.commit()

    logger.info(f"Audit: Offer accepted by candidate. Offer ID: {id}, Candidate ID: {candidate.id}")

    return jsonify({
        "success": True,
        "message": "Offer accepted successfully!",
        "data": offer.to_dict()
    })


@offers_bp.route('/<int:id>/decline', methods=['POST'])
@jwt_required()
@role_required('Candidate')
def decline_offer(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    candidate = Candidate.query.filter_by(user_id=user.id).first()

    offer = Offer.query.get(id)
    if not offer:
        return jsonify({"success": False, "message": "Offer not found"}), 404

    if not candidate or offer.application.candidate_id != candidate.id:
        return jsonify({"success": False, "message": "You do not have permission to decline this offer"}), 403

    if offer.status != 'Sent':
        return jsonify({"success": False, "message": f"Offer cannot be declined from current status '{offer.status}'"}), 400

    offer.status = 'Declined'
    db.session.commit()

    logger.info(f"Audit: Offer declined by candidate. Offer ID: {id}, Candidate ID: {candidate.id}")

    return jsonify({
        "success": True,
        "message": "Offer declined.",
        "data": offer.to_dict()
    })
