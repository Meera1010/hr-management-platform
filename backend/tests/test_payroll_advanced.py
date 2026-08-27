import pytest
from app.services.payroll_tax_engine import TaxRegimeCalculator
from app.services.payroll_payout_export_service import BankPayoutExportService

def test_tax_regime_calculator_new_regime():
    res = TaxRegimeCalculator.calculate_new_regime_tax(1200000.0)
    assert res['gross_income'] == 1200000.0
    assert res['standard_deduction'] == 75000.0
    assert res['taxable_income'] == 1125000.0
    assert res['total_annual_tax'] > 0

def test_tax_regime_calculator_old_regime():
    exemptions = {'sec_80c': 150000.0, 'sec_80d': 25000.0, 'sec_24b': 100000.0}
    res = TaxRegimeCalculator.calculate_old_regime_tax(1200000.0, exemptions)
    assert res['total_exemptions_and_deductions'] == 325000.0
    assert res['taxable_income'] == 875000.0

def test_regime_comparison():
    exemptions = {'sec_80c': 150000.0, 'sec_80d': 25000.0}
    comp = TaxRegimeCalculator.compare_regimes(1500000.0, exemptions)
    assert 'recommended_regime' in comp

def test_bank_payout_export_hdfc():
    payslips = [
        {'period_label': '2026-05', 'employee_id': 1, 'employee_code': 'EMP001', 'employee_name': 'Aarav Sharma', 'net_salary': 75000.0, 'bank_account_no': '501002349012', 'ifsc_code': 'HDFC0000123'}
    ]
    txt = BankPayoutExportService.generate_hdfc_cms_format(payslips)
    assert 'HDFC0000123' in txt
    assert '75000.00' in txt

def test_bank_payout_export_icici():
    payslips = [
        {'period_label': '2026-05', 'employee_id': 1, 'employee_name': 'Aarav Sharma', 'net_salary': 75000.0, 'bank_account_no': '501002349012', 'ifsc_code': 'ICIC0000123'}
    ]
    txt = BankPayoutExportService.generate_icici_cib_format(payslips)
    assert 'ICIC0000123' in txt

def test_payroll_reconciliation():
    payslips = [
        {'gross_earnings': 100000.0, 'pf_deduction': 1800.0, 'professional_tax': 200.0, 'tds_deduction': 8000.0, 'total_deductions': 10000.0, 'net_salary': 90000.0}
    ]
    audit = BankPayoutExportService.reconcile_payroll_batch(payslips)
    assert audit['is_reconciled'] is True
    assert audit['headcount'] == 1
