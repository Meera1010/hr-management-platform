from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.user import User
from app import db
from app.utils.auth import role_required, admin_required, hr_required, recruiter_required

applications_bp = Blueprint('applications_bp', __name__)

@applications_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Candidate')
def create_application():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    candidate = Candidate.query.filter_by(user_id=user_id).first()

    if not candidate or candidate.status == 'Inactive':
        return jsonify({'success': False, 'message': 'Active candidate profile required'}), 403

    data = request.get_json()
    job_id = data.get('job_id')
    cover_letter = data.get('cover_letter', '')

    if not job_id:
        return jsonify({'success': False, 'message': 'Job ID is required'}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'}), 404
        
    if job.status != 'Open':
        return jsonify({'success': False, 'message': 'Job is not open for applications'}), 400

    # Prevent duplicates
    existing = Application.query.filter_by(candidate_id=candidate.id, job_id=job.id).first()
    if existing:
        return jsonify({'success': False, 'message': 'You have already applied for this job'}), 400

    # Generate unique application code
    # Simple logic: count total + 1
    total = Application.query.count()
    app_code = f"APP-{total + 1:04d}"

    new_app = Application(
        application_code=app_code,
        candidate_id=candidate.id,
        job_id=job.id,
        cover_letter=cover_letter
    )

    db.session.add(new_app)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Application submitted successfully',
        'application': new_app.to_dict()
    }), 201


@applications_bp.route('', methods=['GET'])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role.name == 'Employee':
        return jsonify({'success': False, 'message': 'You do not have permission to access this resource'}), 403

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status_filter = request.args.get('status')
    search = request.args.get('search', '')
    job_id_filter = request.args.get('job_id')
    candidate_id_filter = request.args.get('candidate_id')

    query = Application.query

    # Restrict to own applications if candidate
    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate:
            return jsonify({'success': True, 'applications': [], 'total_records': 0, 'total_pages': 0, 'current_page': page})
        query = query.filter_by(candidate_id=candidate.id)
    else:
        # HR/Recruiter/Admin can filter by candidate
        if candidate_id_filter:
            query = query.filter_by(candidate_id=candidate_id_filter)

    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if job_id_filter:
        query = query.filter_by(job_id=job_id_filter)

    if search:
        query = query.join(Candidate).join(Job).filter(
            (Application.application_code.ilike(f"%{search}%")) |
            (Candidate.first_name.ilike(f"%{search}%")) |
            (Candidate.last_name.ilike(f"%{search}%")) |
            (Job.title.ilike(f"%{search}%"))
        )

    pagination = query.order_by(Application.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'success': True,
        'applications': [a.to_dict() for a in pagination.items],
        'total_records': pagination.total,
        'total_pages': pagination.pages,
        'current_page': pagination.page
    })


@applications_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_application(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role.name == 'Employee':
        return jsonify({'success': False, 'message': 'Forbidden'}), 403

    app = Application.query.get_or_404(id)

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or app.candidate_id != candidate.id:
            return jsonify({'success': False, 'message': 'Forbidden'}), 403

    return jsonify({'success': True, 'application': app.to_dict()})


@applications_bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
def update_status(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role.name not in ['Admin', 'HR', 'Recruiter']:
        return jsonify({'success': False, 'message': 'Forbidden'}), 403

    app = Application.query.get_or_404(id)
    data = request.get_json()
    
    new_status = data.get('status')
    valid_statuses = ['Submitted', 'Under Review', 'Shortlisted', 'Rejected', 'Withdrawn', 'Selected']
    
    if new_status and new_status in valid_statuses:
        app.status = new_status
        
    if 'recruiter_notes' in data:
        app.recruiter_notes = data['recruiter_notes']

    db.session.commit()
    return jsonify({'success': True, 'message': 'Status updated', 'application': app.to_dict()})


@applications_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Candidate')
def withdraw_application(id):
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate profile not found'}), 404

    app = Application.query.get_or_404(id)
    if app.candidate_id != candidate.id:
        return jsonify({'success': False, 'message': 'Forbidden'}), 403

    if app.status in ['Rejected', 'Withdrawn', 'Selected']:
        return jsonify({'success': False, 'message': 'Cannot withdraw from this status'}), 400

    app.status = 'Withdrawn'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Application withdrawn successfully', 'application': app.to_dict()})


@applications_bp.route('/<int:id>/shortlist', methods=['PATCH'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def shortlist_application(id):
    user_id = get_jwt_identity()
    app = Application.query.get(id)
    if not app:
        return jsonify({'success': False, 'message': 'Application not found'}), 404

    app.status = 'Shortlisted'
    db.session.commit()

    logger = logging.getLogger('audit')
    logger.info(f"Audit: Candidate shortlisted. Application ID: {id}, By User: {user_id}")

    return jsonify({
        'success': True,
        'message': 'Candidate shortlisted successfully',
        'application': app.to_dict()
    })
