import logging
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.models.job import Job
from app.services.candidate_ranker import CandidateRanker
from app.utils.auth import role_required

logger = logging.getLogger('audit')
ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/jobs/<int:job_id>/rank-candidates', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def get_candidate_rankings(job_id):
    user_id = get_jwt_identity()
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404

    rankings = CandidateRanker.rank_all_candidates_for_job(job_id)

    logger.info(f"Audit: Candidate rankings generated for Job ID {job_id} by User ID {user_id}")

    return jsonify({
        "success": True,
        "data": {
            "job_id": job.id,
            "job_title": job.title,
            "job_code": job.job_code,
            "candidates": rankings
        }
    })
