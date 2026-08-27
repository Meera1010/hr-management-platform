from flask import Blueprint, jsonify, request
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.employee import Employee
from app.services.career_recommender import CareerRecommender
from app.utils.auth import token_required

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@recommendations_bp.route('/my-recommendations', methods=['GET'])
@token_required
def get_my_career_recommendations(current_user):
    """
    Get recommended jobs for the current logged-in Candidate or Employee.
    Analyzes user skills, education, and experience against open jobs.
    """
    user_skills = ''
    user_exp = 0
    user_edu = ''

    if current_user.role == 'Candidate':
        cand = Candidate.query.filter_by(user_id=current_user.id).first()
        if cand:
            user_skills = cand.skills or ''
            user_exp = cand.experience_years or 0
            user_edu = cand.education or ''
    elif current_user.role == 'Employee':
        emp = Employee.query.filter_by(user_id=current_user.id).first()
        if emp:
            user_skills = f"{emp.designation or ''} {emp.department.name if emp.department else ''}"
            user_exp = 3 # Default estimated professional experience
            user_edu = 'Degree'

    open_jobs = Job.query.filter_by(status='Open').all()

    recommendations = []
    for job in open_jobs:
        match_data = CareerRecommender.calculate_job_match(
            user_skills_str=user_skills,
            user_exp_years=user_exp,
            user_education_str=user_edu,
            job=job
        )

        recommendations.append({
            'job_id': job.id,
            'job_code': job.job_code,
            'job_title': job.title,
            'department_name': job.department.name if job.department else 'N/A',
            'location': job.location,
            'employment_type': job.employment_type,
            'match_score': match_data['match_score'],
            'growth_tier': match_data['growth_tier'],
            'matched_skills': match_data['matched_skills'],
            'missing_skills': match_data['missing_skills'],
            'reasoning': match_data['reasoning']
        })

    # Sort descending by match_score
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({
        'success': True,
        'count': len(recommendations),
        'recommendations': recommendations
    }), 200

@recommendations_bp.route('/job-matches/<int:job_id>', methods=['GET'])
@token_required
def get_job_candidate_matches(current_user, job_id):
    """
    Get recommended candidates for a specific Job position (decision support).
    """
    job = Job.query.get_or_404(job_id)
    candidates = Candidate.query.filter_by(status='Available').all()

    matches = []
    for cand in candidates:
        match_data = CareerRecommender.calculate_job_match(
            user_skills_str=cand.skills,
            user_exp_years=cand.experience_years,
            user_education_str=cand.education,
            job=job
        )

        matches.append({
            'candidate_id': cand.id,
            'candidate_code': cand.candidate_code,
            'candidate_name': f"{cand.first_name} {cand.last_name}",
            'email': cand.email,
            'current_role': cand.current_role,
            'match_score': match_data['match_score'],
            'growth_tier': match_data['growth_tier'],
            'matched_skills': match_data['matched_skills'],
            'missing_skills': match_data['missing_skills'],
            'reasoning': match_data['reasoning']
        })

    matches.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({
        'success': True,
        'job_id': job.id,
        'job_title': job.title,
        'count': len(matches),
        'matches': matches
    }), 200
