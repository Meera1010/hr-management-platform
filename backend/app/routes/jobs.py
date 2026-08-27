from flask import Blueprint, request, jsonify
from app import db
from app.models.job import Job
from app.models.department import Department
from app.models.user import User
from app.utils.auth import admin_required, hr_required, recruiter_required, role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('audit')

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    query = Job.query
    
    # RBAC logic
    if user.role.name in ['Employee', 'Candidate', 'Interviewer']:
        query = query.filter_by(status='Open')
    
    # Filters
    department_id = request.args.get('department_id')
    location = request.args.get('location')
    status = request.args.get('status')
    employment_type = request.args.get('employment_type')
    
    if department_id:
        query = query.filter_by(department_id=department_id)
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    if status and user.role.name in ['Admin', 'HR', 'Recruiter']:
        query = query.filter_by(status=status)
    if employment_type:
        query = query.filter_by(employment_type=employment_type)
        
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        "success": True,
        "data": [job.to_dict() for job in pagination.items],
        "current_page": page,
        "total_records": pagination.total,
        "total_pages": pagination.pages
    }), 200

@jobs_bp.route('/search', methods=['GET'])
@jwt_required()
def search_jobs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    q = request.args.get('q', '')
    
    query = Job.query
    if user.role.name in ['Employee', 'Candidate', 'Interviewer']:
        query = query.filter_by(status='Open')
        
    if q:
        query = query.filter(
            db.or_(
                Job.title.ilike(f'%{q}%'),
                Job.job_code.ilike(f'%{q}%'),
                Job.location.ilike(f'%{q}%')
            )
        )
        
    jobs = query.all()
    return jsonify({
        "success": True,
        "data": [job.to_dict() for job in jobs]
    }), 200

@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404
        
    if user.role.name in ['Employee', 'Candidate', 'Interviewer'] and job.status != 'Open':
        return jsonify({"success": False, "message": "You do not have permission to access this resource"}), 403
        
    return jsonify({"success": True, "data": job.to_dict()}), 200

@jobs_bp.route('/', methods=['POST'])
@recruiter_required()
def create_job():
    data = request.get_json()
    
    required_fields = ['title', 'department_id', 'description', 'job_code']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"{field.replace('_', ' ').capitalize()} is required"}), 400
            
    if Job.query.filter_by(job_code=data['job_code']).first():
        return jsonify({"success": False, "message": "Job code must be unique"}), 400
        
    if not Department.query.get(data['department_id']):
        return jsonify({"success": False, "message": "Invalid department"}), 400
        
    valid_emp_types = ['Full Time', 'Part Time', 'Contract', 'Internship']
    if data.get('employment_type') and data['employment_type'] not in valid_emp_types:
        return jsonify({"success": False, "message": "Invalid employment type"}), 400
        
    valid_statuses = ['Draft', 'Open', 'Closed', 'Archived']
    if data.get('status') and data['status'] not in valid_statuses:
        return jsonify({"success": False, "message": "Invalid status"}), 400
        
    user_id = get_jwt_identity()
    
    job = Job(
        job_code=data['job_code'],
        title=data['title'],
        department_id=data['department_id'],
        description=data['description'],
        responsibilities=data.get('responsibilities'),
        required_skills=data.get('required_skills'),
        preferred_skills=data.get('preferred_skills'),
        experience_required=data.get('experience_required'),
        education_required=data.get('education_required'),
        location=data.get('location'),
        employment_type=data.get('employment_type'),
        salary_range=data.get('salary_range'),
        status=data.get('status', 'Draft'),
        created_by=user_id
    )
    
    if data.get('application_deadline'):
        from datetime import datetime
        try:
            job.application_deadline = datetime.strptime(data['application_deadline'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"success": False, "message": "Invalid application deadline format"}), 400
            
    db.session.add(job)
    db.session.commit()
    
    logger.info(f"Audit: Job created. Job ID: {job.id}, Job Code: {job.job_code}, Created By: {user_id}")
    
    return jsonify({"success": True, "data": job.to_dict()}), 201

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@recruiter_required()
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404
        
    data = request.get_json()
    
    if 'job_code' in data and data['job_code'] != job.job_code:
        if Job.query.filter_by(job_code=data['job_code']).first():
            return jsonify({"success": False, "message": "Job code must be unique"}), 400
        job.job_code = data['job_code']
        
    if 'department_id' in data:
        if not Department.query.get(data['department_id']):
            return jsonify({"success": False, "message": "Invalid department"}), 400
        job.department_id = data['department_id']
        
    if 'title' in data: job.title = data['title']
    if 'description' in data: job.description = data['description']
    if 'responsibilities' in data: job.responsibilities = data['responsibilities']
    if 'required_skills' in data: job.required_skills = data['required_skills']
    if 'preferred_skills' in data: job.preferred_skills = data['preferred_skills']
    if 'experience_required' in data: job.experience_required = data['experience_required']
    if 'education_required' in data: job.education_required = data['education_required']
    if 'location' in data: job.location = data['location']
    
    if 'employment_type' in data:
        valid_emp_types = ['Full Time', 'Part Time', 'Contract', 'Internship']
        if data['employment_type'] not in valid_emp_types:
            return jsonify({"success": False, "message": "Invalid employment type"}), 400
        job.employment_type = data['employment_type']
        
    if 'salary_range' in data: job.salary_range = data['salary_range']
    
    if 'application_deadline' in data:
        from datetime import datetime
        if data['application_deadline']:
            try:
                job.application_deadline = datetime.strptime(data['application_deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"success": False, "message": "Invalid application deadline format"}), 400
        else:
            job.application_deadline = None
            
    db.session.commit()
    
    user_id = get_jwt_identity()
    logger.info(f"Audit: Job updated. Job ID: {job.id}, Updated By: {user_id}")
    
    return jsonify({"success": True, "data": job.to_dict()}), 200

@jobs_bp.route('/<int:job_id>/status', methods=['PATCH'])
@recruiter_required()
def change_job_status(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404
        
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['Draft', 'Open', 'Closed', 'Archived']
    if new_status not in valid_statuses:
        return jsonify({"success": False, "message": "Invalid status"}), 400
        
    old_status = job.status
    job.status = new_status
    db.session.commit()
    
    user_id = get_jwt_identity()
    logger.info(f"Audit: Job status changed. Job ID: {job.id}, Old Status: {old_status}, New Status: {new_status}, Changed By: {user_id}")
    
    return jsonify({"success": True, "data": job.to_dict()}), 200

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@hr_required()
def archive_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404
        
    job.status = 'Archived'
    db.session.commit()
    
    user_id = get_jwt_identity()
    logger.info(f"Audit: Job archived. Job ID: {job.id}, Archived By: {user_id}")
    
    return jsonify({"success": True, "message": "Job archived successfully"}), 200
