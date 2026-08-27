from flask import Blueprint, jsonify
from app import db
from app.models.application import Application
from app.models.employee import Employee
from app.models.job import Job
from app.models.department import Department
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.performance_review import PerformanceReview
from app.models.leave_request import LeaveRequest
from app.utils.auth import token_required, role_required

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/overview', methods=['GET'])
@token_required
@role_required(['Admin', 'HR', 'Recruiter'])
def get_analytics_overview(current_user):
    """
    Returns aggregated recruitment and HR workforce analytics.
    """
    # 1. Recruitment Funnel
    total_apps = Application.query.count()
    under_review = Application.query.filter_by(status='Under Review').count()
    shortlisted = Application.query.filter_by(status='Shortlisted').count()
    interviewed = Interview.query.filter_by(status='Completed').count()
    offers_made = Offer.query.count()
    offers_accepted = Offer.query.filter_by(status='Accepted').count()

    funnel = {
        'total_applications': total_apps,
        'under_review': under_review,
        'shortlisted': shortlisted,
        'interviewed': interviewed,
        'offers_made': offers_made,
        'hired': offers_accepted
    }

    # 2. Department Breakdown & Headcount
    departments_analytics = []
    depts = Department.query.all()
    for d in depts:
        emp_count = Employee.query.filter_by(department_id=d.id, status='Active').count()
        job_count = Job.query.filter_by(department_id=d.id, status='Open').count()
        departments_analytics.append({
            'department_id': d.id,
            'name': d.name,
            'employee_count': emp_count,
            'open_jobs': job_count
        })

    # 3. Employment Type Distribution
    full_time = Employee.query.filter_by(employment_type='Full Time', status='Active').count()
    part_time = Employee.query.filter_by(employment_type='Part Time', status='Active').count()
    contract = Employee.query.filter_by(employment_type='Contract', status='Active').count()
    intern = Employee.query.filter_by(employment_type='Intern', status='Active').count()

    employment_types = {
        'full_time': full_time,
        'part_time': part_time,
        'contract': contract,
        'intern': intern
    }

    # 4. Performance Summary Overview
    reviews = PerformanceReview.query.filter_by(status='Completed').all()
    avg_performance = round(sum(r.overall_score for r in reviews) / len(reviews), 2) if reviews else 0.0

    # 5. Leave Requests Summary
    total_leaves = LeaveRequest.query.count()
    approved_leaves = LeaveRequest.query.filter_by(status='Approved').count()
    pending_leaves = LeaveRequest.query.filter_by(status='Pending').count()
    rejected_leaves = LeaveRequest.query.filter_by(status='Rejected').count()

    leaves_summary = {
        'total': total_leaves,
        'approved': approved_leaves,
        'pending': pending_leaves,
        'rejected': rejected_leaves
    }

    return jsonify({
        'success': True,
        'analytics': {
            'funnel': funnel,
            'departments': departments_analytics,
            'employment_types': employment_types,
            'average_performance_score': avg_performance,
            'leaves': leaves_summary
        }
    }), 200
