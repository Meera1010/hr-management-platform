import pytest
from datetime import date
from app.services.onboarding_exit_workflow_engine import LifecycleWorkflowEngine

def test_gratuity_calculation_eligible():
    gratuity = LifecycleWorkflowEngine.calculate_gratuity(100000.0, 7.5)
    expected = round((15.0 * 100000.0 * 7.5) / 26.0, 2)
    assert gratuity == expected

def test_gratuity_calculation_ineligible():
    gratuity = LifecycleWorkflowEngine.calculate_gratuity(100000.0, 3.2)
    assert gratuity == 0.0

def test_notice_period_compliance():
    res = LifecycleWorkflowEngine.calculate_notice_period_compliance(
        joining_date=date(2020, 1, 1),
        resignation_date=date(2026, 5, 1),
        requested_lwd=date(2026, 6, 1),
        required_notice_days=60
    )
    assert res['shortfall_days'] == 29
    assert res['is_compliant'] is False

def test_exit_clearance_readiness():
    readiness = LifecycleWorkflowEngine.evaluate_exit_clearance_readiness([
        {'department_name': 'IT', 'status': 'Cleared', 'dues_amount': 0.0},
        {'department_name': 'Finance', 'status': 'Cleared', 'dues_amount': 0.0}
    ])
    assert readiness['ready_for_fnf'] is True
