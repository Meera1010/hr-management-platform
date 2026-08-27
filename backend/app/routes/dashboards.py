from flask import Blueprint, jsonify
from app.models.employee import Employee
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.leave_request import LeaveRequest
from app.models.attendance import Attendance
from app.models.department import Department
from app.models.training import TrainingAssignment
from app.utils.auth import token_required

dashboards_bp = Blueprint('dashboards', __name__, url_prefix='/api/dashboards')

@dashboards_bp.route('/stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    role = current_user.role.name if (current_user and current_user.role) else ''

    stats = {
        'role': role,
        'metrics': {},
        'charts': {},
        'recent_activity': []
    }

    if role in ['Admin', 'HR']:
        total_emp = Employee.query.count()
        active_emp = Employee.query.filter_by(status='Active').count()
        total_dept = Department.query.count()
        open_jobs = Job.query.filter_by(status='Open').count()
        pending_leaves = LeaveRequest.query.filter_by(status='Pending').count()
        total_apps = Application.query.count()
        
        # Dept breakdown
        dept_counts = []
        for d in Department.query.all():
            c = Employee.query.filter_by(department_id=d.id).count()
            dept_counts.append({'name': d.name, 'count': c})

        stats['metrics'] = {
            'total_employees': total_emp,
            'active_employees': active_emp,
            'departments_count': total_dept,
            'open_jobs': open_jobs,
            'pending_leaves': pending_leaves,
            'total_applications': total_apps
        }
        stats['charts'] = {
            'department_distribution': dept_counts
        }

    elif role == 'Recruiter':
        open_jobs = Job.query.filter_by(status='Open').count()
        total_candidates = Candidate.query.count()
        total_apps = Application.query.count()
        shortlisted_apps = Application.query.filter_by(status='Shortlisted').count()
        upcoming_interviews = Interview.query.filter_by(status='Scheduled').count()
        offers_sent = Offer.query.filter_by(status='Sent').count()

        stats['metrics'] = {
            'active_jobs': open_jobs,
            'total_candidates': total_candidates,
            'total_applications': total_apps,
            'shortlisted_candidates': shortlisted_apps,
            'upcoming_interviews': upcoming_interviews,
            'offers_sent': offers_sent
        }

    elif role == 'Employee':
        emp = Employee.query.filter_by(user_id=current_user.id).first()
        if emp:
            my_leaves = LeaveRequest.query.filter_by(employee_id=emp.id).all()
            pending_leaves = sum(1 for l in my_leaves if l.status == 'Pending')
            approved_leaves = sum(1 for l in my_leaves if l.status == 'Approved')
            
            my_trainings = TrainingAssignment.query.filter_by(employee_id=emp.id).all()
            completed_trainings = sum(1 for t in my_trainings if t.status == 'Completed')
            assigned_trainings = len(my_trainings)

            stats['metrics'] = {
                'employee_code': emp.employee_code,
                'designation': emp.designation,
                'department': emp.department.name if emp.department else 'N/A',
                'joining_date': emp.joining_date.strftime('%Y-%m-%d') if emp.joining_date else 'N/A',
                'pending_leaves': pending_leaves,
                'approved_leaves': approved_leaves,
                'completed_trainings': completed_trainings,
                'assigned_trainings': assigned_trainings
            }
        else:
            stats['metrics'] = {'info': 'Employee profile pending creation.'}

    elif role == 'Candidate':
        cand = Candidate.query.filter_by(user_id=current_user.id).first()
        if cand:
            my_apps = Application.query.filter_by(candidate_id=cand.id).all()
            app_stats = {
                'total': len(my_apps),
                'under_review': sum(1 for a in my_apps if a.status == 'Under Review'),
                'shortlisted': sum(1 for a in my_apps if a.status == 'Shortlisted'),
                'rejected': sum(1 for a in my_apps if a.status == 'Rejected')
            }
            stats['metrics'] = app_stats
        else:
            stats['metrics'] = {'total': 0, 'under_review': 0, 'shortlisted': 0, 'rejected': 0}

    return jsonify({'success': True, 'data': stats}), 200
