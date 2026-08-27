"""
Timesheet Billability & Overtime (OT) Premium Calculator.
Computes overtime payouts based on standard multipliers (1.5x for weekday OT, 2.0x for holiday/weekend OT)
and validates weekly billable utilization rates.
"""

from typing import Dict, Any, List

class OvertimeCalculator:
    WEEKDAY_OT_MULTIPLIER = 1.5
    WEEKEND_OT_MULTIPLIER = 2.0

    @staticmethod
    def calculate_ot_payout(hourly_base_rate: float, ot_hours: float, is_weekend_or_holiday: bool = False) -> Dict[str, Any]:
        """Calculates overtime claim payout based on standard labor rules."""
        multiplier = OvertimeCalculator.WEEKEND_OT_MULTIPLIER if is_weekend_or_holiday else OvertimeCalculator.WEEKDAY_OT_MULTIPLIER
        effective_hourly_rate = hourly_base_rate * multiplier
        total_payout = round(effective_hourly_rate * ot_hours, 2)

        return {
            'hourly_base_rate': hourly_base_rate,
            'multiplier': multiplier,
            'effective_hourly_rate': effective_hourly_rate,
            'ot_hours': ot_hours,
            'total_payout': total_payout
        }

    @staticmethod
    def calculate_weekly_utilization(logged_entries: List[Dict[str, Any]], target_hours_per_week: float = 40.0) -> Dict[str, Any]:
        """Computes billable vs non-billable utilization rates."""
        total_logged = sum(e.get('hours_logged', 0.0) for e in logged_entries)
        billable_logged = sum(e.get('hours_logged', 0.0) for e in logged_entries if e.get('is_billable'))

        billable_utilization_pct = round((billable_logged / target_hours_per_week * 100.0), 1) if target_hours_per_week > 0 else 0.0
        overall_capacity_pct = round((total_logged / target_hours_per_week * 100.0), 1) if target_hours_per_week > 0 else 0.0

        return {
            'target_hours': target_hours_per_week,
            'total_logged_hours': total_logged,
            'billable_logged_hours': billable_logged,
            'non_billable_hours': total_logged - billable_logged,
            'billable_utilization_pct': min(100.0, billable_utilization_pct),
            'overall_capacity_pct': overall_capacity_pct
        }
