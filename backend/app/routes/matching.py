from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.job_matcher import (
    extract_candidate_skills,
    extract_job_skills,
    calculate_skill_match,
    get_candidate_job_matches,
    rank_candidates_for_job
)
from app.utils.auth import role_required

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/jobs/<int:job_id>/match/<int:candidate_id>', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_job_candidate_match(job_id, candidate_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    # Candidate authorization check
    if user.role.name == 'Candidate':
        user_candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not user_candidate or user_candidate.id != candidate_id:
            return jsonify({"success": False, "message": "You do not have permission to view match details for this candidate"}), 403

    c_skills = extract_candidate_skills(candidate_id)
    j_skills = extract_job_skills(job)
    match_result = calculate_skill_match(c_skills, j_skills)

    return jsonify({
        "success": True,
        "data": {
            "candidate": f"{candidate.first_name} {candidate.last_name}",
            "job": job.title,
            "job_code": job.job_code,
            "match_percentage": match_result["match_percentage"],
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"]
        }
    })


@matching_bp.route('/candidates/<int:candidate_id>/matches', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate')
def get_candidate_matches_endpoint(candidate_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"success": False, "message": "Candidate not found"}), 404

    if user.role.name == 'Candidate':
        user_candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not user_candidate or user_candidate.id != candidate_id:
            return jsonify({"success": False, "message": "You do not have permission to access these candidate matches"}), 403

    matches = get_candidate_job_matches(candidate_id)
    return jsonify({
        "success": True,
        "data": matches
    })


@matching_bp.route('/jobs/<int:job_id>/matches', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def get_job_matches_endpoint(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404

    rankings = rank_candidates_for_job(job_id)
    return jsonify({
        "success": True,
        "data": {
            "job_id": job.id,
            "job_title": job.title,
            "job_code": job.job_code,
            "candidates": rankings
        }
    })
