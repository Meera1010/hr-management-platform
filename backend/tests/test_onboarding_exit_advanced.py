import pytest
from datetime import date
from app.services.onboarding_exit_workflow_engine import LifecycleWorkflowEngine

def test_notice_period_compliance():
    res = LifecycleWorkflowEngine.calculate_notice_period_compliance(
        joining_date=date(2023, 1, 1),
        resignation_date=date(2026, 5, 1),
        requested_lwd=date(2026, 6, 30),
        required_notice_days=60
    )
    assert res['required_notice_days'] == 60
    assert res['actual_notice_days'] == 60
    assert res['is_compliant'] is True

def test_exit_clearance_readiness():
    clearances = [
        {'department_name': 'IT', 'status': 'Cleared', 'dues_amount': 0.0},
        {'department_name': 'HR', 'status': 'Cleared', 'dues_amount': 0.0},
        {'department_name': 'Finance', 'status': 'Cleared', 'dues_amount': 0.0},
        {'department_name': 'Admin', 'status': 'Cleared', 'dues_amount': 0.0},
        {'department_name': 'Reporting Manager', 'status': 'Cleared', 'dues_amount': 0.0}
    ]
    res = LifecycleWorkflowEngine.evaluate_exit_clearance_readiness(clearances)
    assert res['ready_for_fnf'] is True
    assert res['cleared_count'] == 5

def test_gratuity_calculation():
    g1 = LifecycleWorkflowEngine.calculate_gratuity(basic_monthly_salary=50000.0, tenure_years=5.0)
    assert g1 > 0

    g2 = LifecycleWorkflowEngine.calculate_gratuity(basic_monthly_salary=50000.0, tenure_years=2.0)
    assert g2 == 0.0
