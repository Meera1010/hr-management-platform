import pytest
from app.services.timesheet_overtime_engine import OvertimeCalculator

def test_overtime_calculator_weekday():
    res = OvertimeCalculator.calculate_ot_payout(hourly_base_rate=500.0, ot_hours=4.0, is_weekend_or_holiday=False)
    assert res['multiplier'] == 1.5
    assert res['effective_hourly_rate'] == 750.0
    assert res['total_payout'] == 3000.0

def test_overtime_calculator_weekend():
    res = OvertimeCalculator.calculate_ot_payout(hourly_base_rate=500.0, ot_hours=4.0, is_weekend_or_holiday=True)
    assert res['multiplier'] == 2.0
    assert res['effective_hourly_rate'] == 1000.0
    assert res['total_payout'] == 4000.0

def test_weekly_utilization_calculation():
    entries = [
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': False}
    ]
    res = OvertimeCalculator.calculate_weekly_utilization(entries, target_hours_per_week=40.0)
    assert res['total_logged_hours'] == 40.0
    assert res['billable_logged_hours'] == 32.0
    assert res['non_billable_hours'] == 8.0
    assert res['billable_utilization_pct'] == 80.0
