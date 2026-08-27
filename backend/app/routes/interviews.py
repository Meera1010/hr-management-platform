import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.candidate import Candidate
from app.models.application import Application
from app.models.interview import Interview
from app.models.interview_feedback import InterviewFeedback
from app.utils.auth import role_required

logger = logging.getLogger('audit')
interviews_bp = Blueprint('interviews', __name__)

@interviews_bp.route('', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate', 'Interviewer')
def get_interviews():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate:
            return jsonify({"success": True, "data": []})
        
        # Get candidate's interviews
        apps = Application.query.filter_by(candidate_id=candidate.id).all()
        app_ids = [a.id for a in apps]
        interviews = Interview.query.filter(Interview.application_id.in_(app_ids)).order_by(Interview.created_at.desc()).all()
        
        # Strip internal notes for candidates
        data = []
        for item in interviews:
            d = item.to_dict()
            d.pop('notes', None)
            data.append(d)
        return jsonify({"success": True, "data": data})

    else:
        # Admin / HR / Recruiter / Interviewer see all or filtered
        app_id = request.args.get('application_id')
        if app_id:
            interviews = Interview.query.filter_by(application_id=app_id).order_by(Interview.created_at.desc()).all()
        else:
            interviews = Interview.query.order_by(Interview.created_at.desc()).all()

        return jsonify({"success": True, "data": [i.to_dict() for i in interviews]})


@interviews_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Candidate', 'Interviewer')
def get_interview(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    interview = Interview.query.get(id)

    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    if user.role.name == 'Candidate':
        candidate = Candidate.query.filter_by(user_id=user.id).first()
        if not candidate or interview.application.candidate_id != candidate.id:
            return jsonify({"success": False, "message": "You do not have permission to view this interview"}), 403
        data = interview.to_dict()
        data.pop('notes', None)
        return jsonify({"success": True, "data": data})

    return jsonify({"success": True, "data": interview.to_dict()})


@interviews_bp.route('', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def create_interview():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    application_id = data.get('application_id')
    interviewer_name = data.get('interviewer_name')
    interview_type = data.get('interview_type', 'Technical')
    scheduled_date = data.get('scheduled_date')
    scheduled_time = data.get('scheduled_time')
    duration_minutes = data.get('duration_minutes', 45)
    meeting_link = data.get('meeting_link', 'https://example.com/demo-interview')
    notes = data.get('notes', '')

    if not application_id or not interviewer_name or not scheduled_date or not scheduled_time:
        return jsonify({"success": False, "message": "application_id, interviewer_name, scheduled_date, and scheduled_time are required"}), 400

    application = Application.query.get(application_id)
    if not application:
        return jsonify({"success": False, "message": "Application not found"}), 404

    # Scheduling Conflict Validation
    conflict = Interview.query.filter_by(
        interviewer_name=interviewer_name.strip(),
        scheduled_date=scheduled_date.strip(),
        scheduled_time=scheduled_time.strip()
    ).filter(Interview.status != 'Cancelled').first()

    if conflict:
        return jsonify({"success": False, "message": "Interviewer already has an interview at this time"}), 400

    last_int = Interview.query.order_by(Interview.id.desc()).first()
    next_num = (last_int.id + 1) if last_int else 1
    interview_code = f"INT-{next_num:04d}"

    interview = Interview(
        interview_code=interview_code,
        application_id=application_id,
        interviewer_name=interviewer_name.strip(),
        interview_type=interview_type,
        scheduled_date=scheduled_date.strip(),
        scheduled_time=scheduled_time.strip(),
        duration_minutes=int(duration_minutes),
        meeting_link=meeting_link,
        status='Scheduled',
        notes=notes
    )

    db.session.add(interview)
    db.session.commit()

    logger.info(f"Audit: Interview created. Code: {interview.interview_code}, Application ID: {application_id}, Scheduled By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Interview scheduled successfully",
        "data": interview.to_dict()
    }), 201


@interviews_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def update_interview(id):
    user_id = get_jwt_identity()
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    data = request.get_json() or {}

    interviewer_name = data.get('interviewer_name', interview.interviewer_name)
    scheduled_date = data.get('scheduled_date', interview.scheduled_date)
    scheduled_time = data.get('scheduled_time', interview.scheduled_time)

    # Conflict check if date/time/interviewer changed
    if (interviewer_name != interview.interviewer_name or 
        scheduled_date != interview.scheduled_date or 
        scheduled_time != interview.scheduled_time):
        
        conflict = Interview.query.filter_by(
            interviewer_name=interviewer_name.strip(),
            scheduled_date=scheduled_date.strip(),
            scheduled_time=scheduled_time.strip()
        ).filter(Interview.id != id, Interview.status != 'Cancelled').first()

        if conflict:
            return jsonify({"success": False, "message": "Interviewer already has an interview at this time"}), 400

    interview.interviewer_name = interviewer_name
    interview.interview_type = data.get('interview_type', interview.interview_type)
    interview.scheduled_date = scheduled_date
    interview.scheduled_time = scheduled_time
    interview.duration_minutes = int(data.get('duration_minutes', interview.duration_minutes))
    interview.meeting_link = data.get('meeting_link', interview.meeting_link)
    interview.notes = data.get('notes', interview.notes)
    if 'status' in data:
        interview.status = data['status']

    db.session.commit()

    logger.info(f"Audit: Interview updated. ID: {id}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Interview updated successfully",
        "data": interview.to_dict()
    })


@interviews_bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Interviewer')
def update_interview_status(id):
    user_id = get_jwt_identity()
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    data = request.get_json() or {}
    new_status = data.get('status')
    valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'Rescheduled']

    if not new_status or new_status not in valid_statuses:
        return jsonify({"success": False, "message": "Invalid interview status"}), 400

    old_status = interview.status
    interview.status = new_status
    db.session.commit()

    logger.info(f"Audit: Interview status changed. ID: {id}, Old: {old_status}, New: {new_status}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Interview status updated successfully",
        "data": interview.to_dict()
    })


@interviews_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter')
def delete_interview(id):
    user_id = get_jwt_identity()
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    db.session.delete(interview)
    db.session.commit()

    logger.info(f"Audit: Interview deleted. ID: {id}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Interview deleted successfully"
    })


@interviews_bp.route('/<int:id>/feedback', methods=['POST'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Interviewer')
def submit_feedback(id):
    user_id = get_jwt_identity()
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    if interview.feedback:
        return jsonify({"success": False, "message": "Feedback has already been submitted for this interview"}), 400

    data = request.get_json() or {}

    try:
        tech = int(data.get('technical_score', 0))
        comm = int(data.get('communication_score', 0))
        prob = int(data.get('problem_solving_score', 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Scores must be numbers between 1 and 5"}), 400

    for s_name, s_val in [('technical_score', tech), ('communication_score', comm), ('problem_solving_score', prob)]:
        if s_val < 1 or s_val > 5:
            return jsonify({"success": False, "message": f"{s_name} must be an integer between 1 and 5"}), 400

    recommendation = data.get('recommendation')
    valid_recs = ['Strongly Recommend', 'Recommend', 'Neutral', 'Do Not Recommend']
    if not recommendation or recommendation not in valid_recs:
        return jsonify({"success": False, "message": f"Recommendation must be one of: {', '.join(valid_recs)}"}), 400

    comments = data.get('comments', '')

    overall_score = round((tech + comm + prob) / 3.0, 2)

    fb = InterviewFeedback(
        interview_id=interview.id,
        technical_score=tech,
        communication_score=comm,
        problem_solving_score=prob,
        overall_score=overall_score,
        recommendation=recommendation,
        comments=comments
    )

    # Mark interview as Completed
    interview.status = 'Completed'

    db.session.add(fb)
    db.session.commit()

    logger.info(f"Audit: Interview feedback submitted. Interview ID: {id}, Overall Score: {overall_score}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Feedback submitted successfully",
        "data": fb.to_dict()
    }), 201


@interviews_bp.route('/<int:id>/feedback', methods=['GET'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Interviewer')
def get_feedback(id):
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    if not interview.feedback:
        return jsonify({"success": False, "message": "Feedback not found for this interview"}), 404

    return jsonify({
        "success": True,
        "data": interview.feedback.to_dict()
    })


@interviews_bp.route('/<int:id>/feedback', methods=['PUT'])
@jwt_required()
@role_required('Admin', 'HR', 'Recruiter', 'Interviewer')
def update_feedback(id):
    user_id = get_jwt_identity()
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"success": False, "message": "Interview not found"}), 404

    fb = interview.feedback
    if not fb:
        return jsonify({"success": False, "message": "Feedback not found for this interview"}), 404

    data = request.get_json() or {}

    if 'technical_score' in data:
        tech = int(data['technical_score'])
        if 1 <= tech <= 5:
            fb.technical_score = tech
    if 'communication_score' in data:
        comm = int(data['communication_score'])
        if 1 <= comm <= 5:
            fb.communication_score = comm
    if 'problem_solving_score' in data:
        prob = int(data['problem_solving_score'])
        if 1 <= prob <= 5:
            fb.problem_solving_score = prob

    fb.overall_score = fb.calculate_overall_score()

    if 'recommendation' in data and data['recommendation'] in ['Strongly Recommend', 'Recommend', 'Neutral', 'Do Not Recommend']:
        fb.recommendation = data['recommendation']

    if 'comments' in data:
        fb.comments = data['comments']

    db.session.commit()

    logger.info(f"Audit: Interview feedback updated. Interview ID: {id}, By User: {user_id}")

    return jsonify({
        "success": True,
        "message": "Feedback updated successfully",
        "data": fb.to_dict()
    })
