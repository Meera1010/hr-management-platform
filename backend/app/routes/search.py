from flask import Blueprint, request, jsonify
from app.models.employee import Employee
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.department import Department
from app.utils.auth import token_required

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

@search_bp.route('', methods=['GET'])
@token_required
def global_search(current_user):
    query_str = request.args.get('q', '').strip()
    if not query_str or len(query_str) < 2:
        return jsonify({
            'success': True,
            'query': query_str,
            'results': {
                'employees': [],
                'candidates': [],
                'jobs': [],
                'applications': [],
                'departments': []
            }
        }), 200

    q_pattern = f"%{query_str}%"
    role = current_user.role

    results = {
        'employees': [],
        'candidates': [],
        'jobs': [],
        'applications': [],
        'departments': []
    }

    # 1. Search Jobs (accessible to all roles)
    jobs = Job.query.filter(
        Job.title.ilike(q_pattern) |
        Job.job_code.ilike(q_pattern) |
        Job.location.ilike(q_pattern)
    ).limit(10).all()
    results['jobs'] = [{
        'id': j.id,
        'code': j.job_code,
        'title': j.title,
        'location': j.location,
        'status': j.status,
        'type': 'Job'
    } for j in jobs]

    # 2. Search Departments (Admin, HR, Recruiter, Employee)
    if role in ['Admin', 'HR', 'Recruiter', 'Employee']:
        depts = Department.query.filter(
            Department.name.ilike(q_pattern) |
            Department.description.ilike(q_pattern)
        ).limit(10).all()
        results['departments'] = [{
            'id': d.id,
            'name': d.name,
            'type': 'Department'
        } for d in depts]

    # 3. Search Employees (Admin, HR, Recruiter)
    if role in ['Admin', 'HR', 'Recruiter']:
        employees = Employee.query.filter(
            Employee.first_name.ilike(q_pattern) |
            Employee.last_name.ilike(q_pattern) |
            Employee.email.ilike(q_pattern) |
            Employee.employee_code.ilike(q_pattern) |
            Employee.designation.ilike(q_pattern)
        ).limit(10).all()
        results['employees'] = [{
            'id': e.id,
            'code': e.employee_code,
            'name': f"{e.first_name} {e.last_name}",
            'email': e.email,
            'designation': e.designation,
            'department': e.department.name if e.department else 'N/A',
            'type': 'Employee'
        } for e in employees]

    # 4. Search Candidates (Admin, HR, Recruiter)
    if role in ['Admin', 'HR', 'Recruiter']:
        candidates = Candidate.query.filter(
            Candidate.first_name.ilike(q_pattern) |
            Candidate.last_name.ilike(q_pattern) |
            Candidate.email.ilike(q_pattern) |
            Candidate.candidate_code.ilike(q_pattern) |
            Candidate.skills.ilike(q_pattern) |
            Candidate.current_role.ilike(q_pattern)
        ).limit(10).all()
        results['candidates'] = [{
            'id': c.id,
            'code': c.candidate_code,
            'name': f"{c.first_name} {c.last_name}",
            'email': c.email,
            'current_role': c.current_role,
            'status': c.status,
            'type': 'Candidate'
        } for c in candidates]

    # 5. Search Applications (Admin, HR, Recruiter)
    if role in ['Admin', 'HR', 'Recruiter']:
        apps = Application.query.filter(
            Application.application_code.ilike(q_pattern) |
            Application.status.ilike(q_pattern)
        ).limit(10).all()
        results['applications'] = [{
            'id': a.id,
            'code': a.application_code,
            'candidate_name': f"{a.candidate.first_name} {a.candidate.last_name}" if a.candidate else 'N/A',
            'job_title': a.job.title if a.job else 'N/A',
            'status': a.status,
            'type': 'Application'
        } for a in apps]

    total_hits = sum(len(v) for v in results.values())

    return jsonify({
        'success': True,
        'query': query_str,
        'total_hits': total_hits,
        'results': results
    }), 200
