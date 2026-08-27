"""
Enterprise Compliance & Regulatory Statutory Rule Checker Engine.
Evaluates compliance with Shops and Establishment Acts, Equal Remuneration Act,
Maternity Benefit Act (26 weeks paid leave), Factory Act max working hours (48 hrs/week),
Minimum Wages rules, and internal Code of Conduct policy compliance.
"""

from typing import Dict, Any, List
from datetime import date, timedelta

class ComplianceRuleChecker:

    @staticmethod
    def evaluate_maternity_leave_eligibility(service_days: int, requested_leave_weeks: float) -> Dict[str, Any]:
        """
        Maternity Benefit Act 1961 (India):
        - Minimum 80 days of continuous service in the 12 months preceding expected delivery date.
        - Maximum 26 weeks paid maternity leave for first 2 surviving children.
        """
        is_service_eligible = service_days >= 80
        max_allowed_weeks = 26.0
        is_duration_valid = requested_leave_weeks <= max_allowed_weeks

        return {
            'act': 'Maternity Benefit Act 1961',
            'service_days': service_days,
            'is_service_eligible': is_service_eligible,
            'requested_leave_weeks': requested_leave_weeks,
            'max_allowed_weeks': max_allowed_weeks,
            'is_compliant': is_service_eligible and is_duration_valid,
            'remarks': 'Eligible for 26 weeks paid maternity leave' if is_service_eligible and is_duration_valid else 'Ineligible or requested duration exceeds 26 weeks'
        }

    @staticmethod
    def check_max_working_hours_limit(weekly_logged_hours: float) -> Dict[str, Any]:
        """
        Factories Act 1948 & Shops Act Rule:
        - Normal working hours limit: 48 hours per week.
        - Overtime limit: Total hours including OT must not exceed 60 hours in any week.
        """
        standard_limit = 48.0
        max_cap_limit = 60.0

        is_overtime = weekly_logged_hours > standard_limit
        is_breach = weekly_logged_hours > max_cap_limit

        return {
            'weekly_logged_hours': weekly_logged_hours,
            'standard_limit': standard_limit,
            'max_cap_limit': max_cap_limit,
            'is_overtime': is_overtime,
            'is_regulatory_breach': is_breach,
            'status': 'Non-Compliant (Breached Max Hours Cap)' if is_breach else ('Overtime Triggered' if is_overtime else 'Compliant Standard Hours')
        }

    @staticmethod
    def verify_minimum_wage_compliance(basic_monthly_pay: float, minimum_wage_threshold: float = 18000.0) -> Dict[str, Any]:
        """Verifies monthly basic salary against state minimum wage notifications."""
        is_compliant = basic_monthly_pay >= minimum_wage_threshold
        shortfall = max(0.0, minimum_wage_threshold - basic_monthly_pay)

        return {
            'basic_monthly_pay': basic_monthly_pay,
            'minimum_wage_threshold': minimum_wage_threshold,
            'is_compliant': is_compliant,
            'shortfall_amount': round(shortfall, 2)
        }
