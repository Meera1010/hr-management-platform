"""
Onboarding & Resignation Clearance Workflow Rule Engine.
Validates multi-department exit clearance matrices, notice period calculations,
and generates Full & Final (FnF) financial settlement statements.
"""

from typing import Dict, Any, List
from datetime import datetime, date

class LifecycleWorkflowEngine:

    @staticmethod
    def calculate_notice_period_compliance(joining_date: date, resignation_date: date, requested_lwd: date, required_notice_days: int = 60) -> Dict[str, Any]:
        """Calculates actual notice served vs required notice days, and shortfall notice pay deduction."""
        actual_notice_days = (requested_lwd - resignation_date).days
        shortfall_days = max(0, required_notice_days - actual_notice_days)

        is_compliant = shortfall_days == 0

        return {
            'required_notice_days': required_notice_days,
            'actual_notice_days': actual_notice_days,
            'shortfall_days': shortfall_days,
            'is_compliant': is_compliant,
            'shortfall_notice_pay_required': shortfall_days > 0
        }

    @staticmethod
    def evaluate_exit_clearance_readiness(clearances: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates whether all 5 clearance departments have approved the exit."""
        total_depts = len(clearances)
        cleared_depts = sum(1 for c in clearances if c.get('status') == 'Cleared')
        pending_depts = [c.get('department_name') for c in clearances if c.get('status') != 'Cleared']
        total_dues = sum(c.get('dues_amount', 0.0) for c in clearances)

        all_cleared = cleared_depts == total_depts and total_depts > 0

        return {
            'total_departments': total_depts,
            'cleared_count': cleared_depts,
            'pending_departments': pending_depts,
            'total_pending_dues': round(total_dues, 2),
            'ready_for_fnf': all_cleared
        }

    @staticmethod
    def calculate_gratuity(basic_monthly_salary: float, tenure_years: float) -> float:
        """
        Standard Gratuity Calculation formula (India Payment of Gratuity Act):
        (15 * Basic Salary * Tenure Years) / 26
        Applicable if tenure >= 4.8 years (round to 5).
        """
        if tenure_years < 4.8:
            return 0.0

        gratuity = (15.0 * basic_monthly_salary * tenure_years) / 26.0
        return round(gratuity, 2)
