import csv
import io
from flask import Blueprint, jsonify, request, Response
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.application import Application
from app.models.performance_review import PerformanceReview
from app.utils.auth import token_required, role_required

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/headcount', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def headcount_report(current_user):
    export = request.args.get('export') == 'csv'
    employees = Employee.query.order_by(Employee.employee_code.asc()).all()

    data = []
    for emp in employees:
        data.append({
            'Employee Code': emp.employee_code,
            'First Name': emp.first_name,
            'Last Name': emp.last_name,
            'Email': emp.email,
            'Department': emp.department.name if emp.department else 'N/A',
            'Designation': emp.designation,
            'Employment Type': emp.employment_type,
            'Status': emp.status,
            'Joining Date': emp.joining_date.strftime('%Y-%m-%d') if emp.joining_date else 'N/A'
        })

    if export:
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=headcount_report.csv"}
        )

    return jsonify({'success': True, 'count': len(data), 'data': data}), 200

@reports_bp.route('/attendance', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def attendance_report(current_user):
    export = request.args.get('export') == 'csv'
    records = Attendance.query.order_by(Attendance.attendance_date.desc()).all()

    data = []
    for r in records:
        emp = r.employee
        data.append({
            'Date': r.attendance_date,
            'Employee Code': emp.employee_code if emp else 'N/A',
            'Employee Name': f"{emp.first_name} {emp.last_name}" if emp else 'N/A',
            'Status': r.status,
            'Check In': r.check_in or 'N/A',
            'Check Out': r.check_out or 'N/A',
            'Work Hours': r.work_hours if r.work_hours is not None else 'N/A'
        })

    if export:
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=attendance_report.csv"}
        )

    return jsonify({'success': True, 'count': len(data), 'data': data}), 200

@reports_bp.route('/recruitment', methods=['GET'])
@token_required
@role_required(['Admin', 'HR', 'Recruiter'])
def recruitment_report(current_user):
    export = request.args.get('export') == 'csv'
    apps = Application.query.order_by(Application.created_at.desc()).all()

    data = []
    for a in apps:
        data.append({
            'Application Code': a.application_code,
            'Candidate Name': f"{a.candidate.first_name} {a.candidate.last_name}" if a.candidate else 'N/A',
            'Candidate Email': a.candidate.email if a.candidate else 'N/A',
            'Job Title': a.job.title if a.job else 'N/A',
            'Department': a.job.department.name if (a.job and a.job.department) else 'N/A',
            'Status': a.status,
            'Applied Date': a.applied_date.strftime('%Y-%m-%d') if a.applied_date else 'N/A'
        })

    if export:
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=recruitment_report.csv"}
        )

    return jsonify({'success': True, 'count': len(data), 'data': data}), 200

@reports_bp.route('/performance', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def performance_report(current_user):
    export = request.args.get('export') == 'csv'
    reviews = PerformanceReview.query.order_by(PerformanceReview.review_period.desc()).all()

    data = []
    for pr in reviews:
        emp = pr.employee
        data.append({
            'Review Code': pr.review_code,
            'Employee Code': emp.employee_code if emp else 'N/A',
            'Employee Name': f"{emp.first_name} {emp.last_name}" if emp else 'N/A',
            'Department': emp.department.name if (emp and emp.department) else 'N/A',
            'Review Period': pr.review_period,
            'Productivity': pr.productivity_score,
            'Quality': pr.quality_score,
            'Teamwork': pr.teamwork_score,
            'Goal Score': pr.goal_score,
            'Overall Score': pr.overall_score,
            'Status': pr.status
        })

    if export:
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=performance_report.csv"}
        )

    return jsonify({'success': True, 'count': len(data), 'data': data}), 200
