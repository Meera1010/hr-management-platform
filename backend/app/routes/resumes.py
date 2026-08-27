import os
import uuid
import logging
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename

from app import db
from app.models.user import User
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor
from app.utils.auth import role_required

logger = logging.getLogger('audit')
resumes_bp = Blueprint('resumes', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'txt', 'docx'})

@resumes_bp.route('/upload', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def upload_resume():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected for uploading"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Invalid file extension. Allowed extensions: PDF, TXT, DOCX"}), 400

    # Determine target candidate
    candidate_id = request.form.get('candidate_id')
    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate:
            return jsonify({"success": False, "message": "Candidate profile not found for user"}), 404
        candidate_id = candidate.id
    else:
        if not candidate_id:
            return jsonify({"success": False, "message": "candidate_id is required"}), 400
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({"success": False, "message": "Candidate not found"}), 404

    # File size validation
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)
    if file_size > max_size:
        return jsonify({"success": False, "message": f"File size exceeds maximum allowed limit ({max_size // (1024*1024)} MB)"}), 400

    # Safe filename & path traversal prevention
    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit('.', 1)[1].upper() if '.' in original_filename else 'TXT'
    safe_disk_filename = f"cand{candidate_id}_{uuid.uuid4().hex[:10]}.{ext.lower()}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, safe_disk_filename)
    file.save(file_path)

    # Generate Resume code
    last_resume = Resume.query.order_by(Resume.id.desc()).first()
    next_num = (last_resume.id + 1) if last_resume else 1
    resume_code = f"RES-{next_num:04d}"

    # Auto extract text
    extraction = ResumeParser.extract_text(file_path, ext)
    extracted_text = extraction.get('text') if extraction.get('success') else None

    # Auto extract skills if text available
    extracted_skills = []
    if extracted_text:
        extracted_skills = SkillExtractor.extract_skills(extracted_text)

    resume = Resume(
        resume_code=resume_code,
        candidate_id=candidate_id,
        filename=safe_disk_filename,
        file_type=ext,
        file_size=file_size,
        extracted_text=extracted_text,
        status='Parsed' if extracted_text else 'Uploaded'
    )
    resume.set_skills_list(extracted_skills)

    db.session.add(resume)
    db.session.commit()

    logger.info(f"Audit: Resume uploaded. Resume ID: {resume.id}, Code: {resume.resume_code}, Candidate ID: {candidate_id}, Uploaded By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Resume uploaded and processed successfully",
        "data": resume.to_dict()
    }), 201


@resumes_bp.route('', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_resumes():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate:
            return jsonify({"success": True, "data": []})
        resumes = Resume.query.filter_by(candidate_id=candidate.id).order_by(Resume.uploaded_at.desc()).all()
    else:
        # HR / Recruiter / Admin sees all
        candidate_id = request.args.get('candidate_id')
        if candidate_id:
            resumes = Resume.query.filter_by(candidate_id=candidate_id).order_by(Resume.uploaded_at.desc()).all()
        else:
            resumes = Resume.query.order_by(Resume.uploaded_at.desc()).all()

    return jsonify({
        "success": True,
        "data": [r.to_dict() for r in resumes]
    })


@resumes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_resume(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    resume = Resume.query.get(id)

    if not resume:
        return jsonify({"success": False, "message": "Resume not found"}), 404

    # Ownership check for Candidate
    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or resume.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to access this resume"}), 403

    return jsonify({
        "success": True,
        "data": resume.to_dict()
    })


@resumes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def delete_resume(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    resume = Resume.query.get(id)

    if not resume:
        return jsonify({"success": False, "message": "Resume not found"}), 404

    # Ownership check
    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or resume.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to delete this resume"}), 403

    # Remove physical file if exists
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, resume.filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to delete resume file: {str(e)}")

    db.session.delete(resume)
    db.session.commit()

    logger.info(f"Audit: Resume deleted. Resume ID: {id}, Deleted By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Resume deleted successfully"
    })


@resumes_bp.route('/<int:id>/download', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def download_resume(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    resume = Resume.query.get(id)

    if not resume:
        return jsonify({"success": False, "message": "Resume not found"}), 404

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or resume.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to download this resume"}), 403

    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, resume.filename)

    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "Resume file missing from storage"}), 404

    return send_from_directory(upload_folder, resume.filename, as_attachment=True, download_name=f"{resume.resume_code}_{resume.filename}")


@resumes_bp.route('/<int:id>/extract-skills', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def extract_resume_skills(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    resume = Resume.query.get(id)

    if not resume:
        return jsonify({"success": False, "message": "Resume not found"}), 404

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or resume.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to modify this resume"}), 403

    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, resume.filename)

    # Re-extract text if not populated
    if not resume.extracted_text and os.path.exists(file_path):
        extraction = ResumeParser.extract_text(file_path, resume.file_type)
        if extraction.get('success'):
            resume.extracted_text = extraction['text']

    if not resume.extracted_text:
        return jsonify({"success": False, "message": "Unable to extract text from resume for skill analysis"}), 400

    # Extract skills
    skills = SkillExtractor.extract_skills(resume.extracted_text)
    resume.set_skills_list(skills)
    resume.status = 'Parsed'
    db.session.commit()

    logger.info(f"Audit: Resume skills extracted. Resume ID: {id}, Extracted Skills Count: {len(skills)}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Skills extracted successfully",
        "data": {
            "resume_id": resume.id,
            "skills": skills
        }
    })
