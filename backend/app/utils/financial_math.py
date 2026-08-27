"""
Financial Mathematics & Payroll Calculation Utility Functions.
Provides precise rounding, loan amortization schedules, compounding formulas,
proration algorithms, and multi-currency exchange conversion functions for HR platform calculations.
"""

from typing import Dict, Any, List
import math

def calculate_prorated_salary(monthly_gross: float, total_working_days: int, actual_payable_days: float) -> float:
    """Calculates prorated monthly earnings based on working days attendance."""
    if total_working_days <= 0:
        return 0.0
    daily_rate = monthly_gross / float(total_working_days)
    prorated = daily_rate * actual_payable_days
    return round(prorated, 2)

def calculate_loan_emi(principal: float, annual_interest_rate_pct: float, tenure_months: int) -> Dict[str, Any]:
    """Calculates monthly Equal Monthly Installment (EMI) for employee salary advance loans."""
    if principal <= 0 or tenure_months <= 0:
        return {'monthly_emi': 0.0, 'total_payable': 0.0, 'total_interest': 0.0}

    monthly_rate = (annual_interest_rate_pct / 100.0) / 12.0

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months)) / (math.pow(1 + monthly_rate, tenure_months) - 1)

    total_payable = emi * tenure_months
    total_interest = total_payable - principal

    return {
        'principal': round(principal, 2),
        'annual_interest_rate_pct': annual_interest_rate_pct,
        'tenure_months': tenure_months,
        'monthly_emi': round(emi, 2),
        'total_payable': round(total_payable, 2),
        'total_interest': round(total_interest, 2)
    }

def generate_amortization_schedule(principal: float, annual_interest_rate_pct: float, tenure_months: int) -> List[Dict[str, Any]]:
    """Generates monthly loan repayment amortization schedule breakdown."""
    emi_info = calculate_loan_emi(principal, annual_interest_rate_pct, tenure_months)
    monthly_emi = emi_info['monthly_emi']
    monthly_rate = (annual_interest_rate_pct / 100.0) / 12.0

    balance = principal
    schedule = []

    for month in range(1, tenure_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_emi - interest_payment
        balance = max(0.0, balance - principal_payment)

        schedule.append({
            'month': month,
            'beginning_balance': round(balance + principal_payment, 2),
            'emi': monthly_emi,
            'principal_component': round(principal_payment, 2),
            'interest_component': round(interest_payment, 2),
            'ending_balance': round(balance, 2)
        })

    return schedule

def convert_currency(amount: float, from_currency: str, to_currency: str = 'INR') -> float:
    """Utility function for multi-currency expense conversions (Fictional FX rates)."""
    fx_rates = {
        'USD': 83.5,
        'EUR': 90.2,
        'GBP': 105.8,
        'AED': 22.7,
        'SGD': 61.5,
        'INR': 1.0
    }
    from_rate = fx_rates.get(from_currency.upper(), 1.0)
    to_rate = fx_rates.get(to_currency.upper(), 1.0)

    amount_in_inr = amount * from_rate
    converted_amount = amount_in_inr / to_rate
    return round(converted_amount, 2)
