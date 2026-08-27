"""
Payroll Formula Evaluator & Allowance Component Rule Engine.
Evaluates custom algebraic salary component formulas, Flexi-Benefit Allowances (FBA),
and Provident Fund voluntary contributions (VPF).
"""

from typing import Dict, Any, List

class PayrollFormulaEvaluator:

    @staticmethod
    def evaluate_flexi_benefits(annual_ctc: float, selected_fba: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluates Flexi-Benefit Allowances (FBA):
        - Food Allowance (Tax free up to 26,400/year)
        - Internet / Communication Allowance (Tax free up to 36,000/year)
        - Learning & Development Allowance (Tax free up to 50,000/year)
        - Fuel & Conveyance Allowance (Tax free up to 48,000/year)
        """
        food = min(float(selected_fba.get('food_allowance', 0.0)), 26400.0)
        internet = min(float(selected_fba.get('internet_allowance', 0.0)), 36000.0)
        lnd = min(float(selected_fba.get('lnd_allowance', 0.0)), 50000.0)
        fuel = min(float(selected_fba.get('fuel_allowance', 0.0)), 48000.0)

        total_fba = food + internet + lnd + fuel
        monthly_fba = total_fba / 12.0

        return {
            'annual_ctc': annual_ctc,
            'annual_total_fba': round(total_fba, 2),
            'monthly_total_fba': round(monthly_fba, 2),
            'breakdown': {
                'food_allowance': food,
                'internet_allowance': internet,
                'lnd_allowance': lnd,
                'fuel_allowance': fuel
            }
        }

    @staticmethod
    def calculate_vpf_contribution(basic_monthly_salary: float, vpf_percentage: float) -> Dict[str, Any]:
        """Calculates Voluntary Provident Fund (VPF) additional contribution above 12% statutory PF."""
        vpf_pct = min(100.0, max(0.0, vpf_percentage))
        statutory_pf = round(min(basic_monthly_salary * 0.12, 1800.0), 2)
        vpf_amount = round(basic_monthly_salary * (vpf_pct / 100.0), 2)

        total_pf_employee = statutory_pf + vpf_amount

        return {
            'basic_monthly_salary': basic_monthly_salary,
            'statutory_pf': statutory_pf,
            'vpf_percentage': vpf_pct,
            'vpf_amount': vpf_amount,
            'total_employee_pf_deduction': total_pf_employee
        }
