import pytest
from datetime import datetime
from app.utils.compliance_rule_checker import ComplianceRuleChecker
from app.utils.skill_gap_matrix_engine import SkillGapMatrixEngine
from app.utils.time_tracking_calculator import TimeTrackingCalculator
from app.utils.audit_trail_serializer import serialize_audit_event
from app.utils.report_data_formatter import ReportDataFormatter

def test_maternity_leave_eligibility():
    res = ComplianceRuleChecker.evaluate_maternity_leave_eligibility(service_days=180, requested_leave_weeks=26.0)
    assert res['is_compliant'] is True
    assert res['max_allowed_weeks'] == 26.0

def test_working_hours_limit():
    res = ComplianceRuleChecker.check_max_working_hours_limit(65.0)
    assert res['is_regulatory_breach'] is True

def test_minimum_wage_compliance():
    res = ComplianceRuleChecker.verify_minimum_wage_compliance(25000.0, 18000.0)
    assert res['is_compliant'] is True
    assert res['shortfall_amount'] == 0.0

def test_team_competency_matrix():
    matrix = SkillGapMatrixEngine.calculate_team_competency_matrix(
        team_skills=[{'employee_id': 1, 'skill_name': 'Python', 'proficiency_level': 4}],
        required_role_skills=[{'skill_name': 'Python', 'min_proficiency': 3}]
    )
    assert matrix['overall_team_coverage_pct'] == 100.0

def test_net_shift_hours():
    t_in = datetime(2026, 5, 1, 9, 0, 0)
    t_out = datetime(2026, 5, 1, 18, 0, 0)
    hours = TimeTrackingCalculator.calculate_net_shift_hours(t_in, t_out, break_minutes=60)
    assert hours['gross_hours'] == 9.0
    assert hours['net_hours'] == 8.0

def test_audit_event_serializer():
    event = serialize_audit_event(
        user_id=1,
        user_email='admin@example.com',
        action='UPDATE_SALARY',
        target_entity='EmployeeSalary',
        entity_id=10,
        changes={'ctc': 1200000.0}
    )
    assert event['action'] == 'UPDATE_SALARY'
    assert '1200000.0' in event['changes_json']

def test_report_data_formatter():
    depts = [
        {'code': 'ENG', 'name': 'Engineering', 'employee_count': 10, 'monthly_payroll_cost': 1000000.0}
    ]
    report = ReportDataFormatter.format_headcount_summary(depts)
    assert report['grand_headcount'] == 10
    assert report['rows'][0]['avg_cost_per_employee'] == '₹100,000.00'
