import pytest
from app.services.payroll_tax_engine import TaxRegimeCalculator
from app.services.payroll_payout_export_service import BankPayoutExportService
from app.utils.payroll_formula_evaluator import PayrollFormulaEvaluator

def test_old_tax_regime_slabs_zero_tax():
    result = TaxRegimeCalculator.calculate_old_regime_tax(400000.0, {
        'sec_80c': 150000.0,
        'sec_80d': 25000.0,
        'sec_24b': 50000.0
    })
    assert result['total_annual_tax'] == 0.0
    assert result['monthly_tds'] == 0.0

def test_new_tax_regime_slabs():
    result = TaxRegimeCalculator.calculate_new_regime_tax(1200000.0)
    assert result['taxable_income'] == 1125000.0
    assert result['total_annual_tax'] > 0.0
    assert result['monthly_tds'] == round(result['total_annual_tax'] / 12.0, 2)

def test_payroll_payout_export_format():
    records = [
        {'employee_id': 1, 'employee_code': 'EMP-001', 'period_label': '2026-05', 'bank_account_no': '1234567890', 'net_salary': 75000.0, 'ifsc_code': 'HDFC0001234', 'employee_name': 'Aarav'},
        {'employee_id': 2, 'employee_code': 'EMP-002', 'period_label': '2026-05', 'bank_account_no': '9876543210', 'net_salary': 95000.0, 'ifsc_code': 'ICIC0005678', 'employee_name': 'Meera'}
    ]
    txt = BankPayoutExportService.generate_hdfc_cms_format(records)
    assert 'HDFC0001234' in txt
    assert 'Aarav' in txt

def test_flexi_benefit_allowances():
    fba = PayrollFormulaEvaluator.evaluate_flexi_benefits(1500000.0, {
        'food_allowance': 26400.0,
        'internet_allowance': 36000.0,
        'lnd_allowance': 50000.0
    })
    assert fba['annual_total_fba'] == 112400.0
    assert fba['monthly_total_fba'] == round(112400.0 / 12.0, 2)

def test_vpf_contributions():
    vpf = PayrollFormulaEvaluator.calculate_vpf_contribution(50000.0, 10.0)
    assert vpf['statutory_pf'] == 1800.0
    assert vpf['vpf_amount'] == 5000.0
    assert vpf['total_employee_pf_deduction'] == 6800.0
