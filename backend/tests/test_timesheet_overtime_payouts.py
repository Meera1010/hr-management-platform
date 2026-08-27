import pytest
from app.services.timesheet_overtime_engine import OvertimeCalculator

def test_overtime_payout_weekday():
    ot = OvertimeCalculator.calculate_ot_payout(hourly_base_rate=500.0, ot_hours=4.0, is_weekend_or_holiday=False)
    # Rate: 1.5x => 750/hr * 4 = 3000
    assert ot['multiplier'] == 1.5
    assert ot['total_payout'] == 3000.0

def test_overtime_payout_weekend():
    ot = OvertimeCalculator.calculate_ot_payout(hourly_base_rate=500.0, ot_hours=4.0, is_weekend_or_holiday=True)
    # Rate: 2.0x => 1000/hr * 4 = 4000
    assert ot['multiplier'] == 2.0
    assert ot['total_payout'] == 4000.0

def test_weekly_utilization_rate():
    entries = [
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': True},
        {'hours_logged': 8.0, 'is_billable': False}
    ]
    util = OvertimeCalculator.calculate_weekly_utilization(entries, target_hours_per_week=40.0)
    assert util['billable_utilization_pct'] == 80.0
    assert util['overall_capacity_pct'] == 100.0
