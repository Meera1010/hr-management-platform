import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.candidate import Candidate
from app.models.user import User
from app import db
from app.utils.auth import role_required, admin_required, hr_required, recruiter_required
import re

candidates_bp = Blueprint('candidates', __name__)
logger = logging.getLogger(__name__)

# Basic email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@candidates_bp.route('', methods=['POST'])
@recruiter_required()
def create_candidate():
    data = request.get_json()
    
    # Validation
    if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({'success': False, 'message': 'First name, last name, and email are required'}), 400
        
    if not is_valid_email(data.get('email')):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
    if Candidate.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Candidate email already exists'}), 400
        
    if data.get('candidate_code') and Candidate.query.filter_by(candidate_code=data['candidate_code']).first():
        return jsonify({'success': False, 'message': 'Candidate code already exists'}), 400
        
    if data.get('experience_years') is not None and float(data['experience_years']) < 0:
        return jsonify({'success': False, 'message': 'Experience must be zero or greater'}), 400
        
    status = data.get('status', 'Available')
    valid_statuses = ['Active', 'Inactive', 'Available', 'Hired', 'Rejected']
    if status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
    new_candidate = Candidate(
        candidate_code=data.get('candidate_code'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        education=data.get('education'),
        experience_years=data.get('experience_years', 0),
        current_role=data.get('current_role'),
        skills=data.get('skills'),
        certifications=data.get('certifications'),
        location=data.get('location'),
        status=status,
        user_id=data.get('user_id')
    )
    
    db.session.add(new_candidate)
    db.session.commit()
    
    # Audit log
    current_user_id = get_jwt_identity()
    logger.info(f"User {current_user_id} created Candidate {new_candidate.id} - {new_candidate.candidate_code}")
    
    return jsonify({
        'success': True,
        'message': 'Candidate created successfully',
        'candidate': new_candidate.to_dict()
    }), 201

@candidates_bp.route('', methods=['GET'])
@recruiter_required()
def get_candidates():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    query = Candidate.query
    
    # Simple search
    search = request.args.get('search', '')
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                Candidate.first_name.ilike(search_pattern),
                Candidate.last_name.ilike(search_pattern),
                Candidate.email.ilike(search_pattern),
                Candidate.candidate_code.ilike(search_pattern),
                Candidate.current_role.ilike(search_pattern),
                Candidate.skills.ilike(search_pattern)
            )
        )
        
    # Filtering
    status = request.args.get('status')
    if status:
        query = query.filter(Candidate.status == status)
        
    location = request.args.get('location')
    if location:
        query = query.filter(Candidate.location.ilike(f"%{location}%"))
        
    experience = request.args.get('experience_years')
    if experience:
        try:
            exp_val = int(experience)
            query = query.filter(Candidate.experience_years >= exp_val)
        except ValueError:
            pass
            
    education = request.args.get('education')
    if education:
        query = query.filter(Candidate.education.ilike(f"%{education}%"))
        
    skills = request.args.get('skills')
    if skills:
        query = query.filter(Candidate.skills.ilike(f"%{skills}%"))
    
    pagination = query.order_by(Candidate.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    
    candidates = [c.to_dict() for c in pagination.items]
    
    return jsonify({
        'success': True,
        'candidates': candidates,
        'current_page': pagination.page,
        'total_pages': pagination.pages,
        'total_records': pagination.total
    }), 200

@candidates_bp.route('/<int:id>', methods=['GET'])
@recruiter_required()
def get_candidate(id):
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate not found'}), 404
        
    return jsonify({
        'success': True,
        'candidate': candidate.to_dict()
    }), 200

@candidates_bp.route('/me', methods=['GET'])
@role_required('Candidate')
def get_my_profile():
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate profile not found'}), 404
        
    return jsonify({
        'success': True,
        'candidate': candidate.to_dict()
    }), 200

@candidates_bp.route('/me', methods=['PUT'])
@role_required('Candidate')
def update_my_profile():
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate profile not found'}), 404
        
    data = request.get_json()
    
    # Restricted fields that a candidate cannot change: status, candidate_code
    if 'first_name' in data: candidate.first_name = data['first_name']
    if 'last_name' in data: candidate.last_name = data['last_name']
    if 'phone' in data: candidate.phone = data['phone']
    if 'education' in data: candidate.education = data['education']
    if 'experience_years' in data: candidate.experience_years = data['experience_years']
    if 'current_role' in data: candidate.current_role = data['current_role']
    if 'skills' in data: candidate.skills = data['skills']
    if 'certifications' in data: candidate.certifications = data['certifications']
    if 'location' in data: candidate.location = data['location']
    
    db.session.commit()
    
    logger.info(f"Candidate {candidate.id} updated their own profile")
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully',
        'candidate': candidate.to_dict()
    }), 200

@candidates_bp.route('/<int:id>', methods=['PUT'])
@recruiter_required()
def update_candidate(id):
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate not found'}), 404
        
    data = request.get_json()
    
    if 'email' in data and data['email'] != candidate.email:
        if not is_valid_email(data['email']):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        if Candidate.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Candidate email already exists'}), 400
        candidate.email = data['email']
        
    if 'experience_years' in data and data['experience_years'] is not None:
        if float(data['experience_years']) < 0:
            return jsonify({'success': False, 'message': 'Experience must be zero or greater'}), 400
        candidate.experience_years = data['experience_years']
            
    if 'status' in data:
        valid_statuses = ['Active', 'Inactive', 'Available', 'Hired', 'Rejected']
        if data['status'] not in valid_statuses:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        if data['status'] != candidate.status:
            logger.info(f"Candidate {candidate.id} status changed from {candidate.status} to {data['status']}")
            candidate.status = data['status']
            
    # Update other fields
    for field in ['first_name', 'last_name', 'phone', 'education', 'current_role', 'skills', 'certifications', 'location', 'candidate_code', 'user_id']:
        if field in data:
            setattr(candidate, field, data[field])
            
    db.session.commit()
    
    current_user_id = get_jwt_identity()
    logger.info(f"User {current_user_id} updated Candidate {candidate.id}")
    
    return jsonify({
        'success': True,
        'message': 'Candidate updated successfully',
        'candidate': candidate.to_dict()
    }), 200

@candidates_bp.route('/<int:id>', methods=['DELETE'])
@recruiter_required()
def deactivate_candidate(id):
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'success': False, 'message': 'Candidate not found'}), 404
        
    candidate.status = 'Inactive'
    db.session.commit()
    
    current_user_id = get_jwt_identity()
    logger.info(f"User {current_user_id} deactivated Candidate {candidate.id}")
    
    return jsonify({
        'success': True,
        'message': 'Candidate deactivated successfully'
    }), 200
