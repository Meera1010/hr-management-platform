import pytest
from app.models.payroll import SalaryStructure, EmployeeSalary, PayrollRun, PaySlip, TaxDeclaration
from app.services.payroll_service import PayrollService

def test_salary_calculation_service():
    calc = PayrollService.calculate_salary_breakdown(1200000.0)
    assert calc['monthly_gross'] == 100000.0
    assert calc['basic_pay'] == 40000.0
    assert calc['hra'] == 20000.0
    assert calc['net_salary'] > 0

def test_salary_structure_api(client, admin_headers):
    res = client.post('/api/payroll/structures', json={
        'title': 'Senior Tech Scale',
        'code': 'TECH-SR-01',
        'base_salary_pct': 45.0,
        'hra_pct': 25.0
    }, headers=admin_headers)

    assert res.status_code == 201
    assert res.json['structure']['code'] == 'TECH-SR-01'

    get_res = client.get('/api/payroll/structures', headers=admin_headers)
    assert get_res.status_code == 200
    assert len(get_res.json['structures']) > 0

def test_employee_salary_configuration(client, admin_headers):
    res = client.post('/api/payroll/employee-salaries', json={
        'employee_id': 1,
        'annual_ctc': 1500000.0,
        'bank_name': 'HDFC Bank',
        'bank_account_no': '501009876543'
    }, headers=admin_headers)

    assert res.status_code == 200
    assert res.json['salary']['annual_ctc'] == 1500000.0

def test_payroll_run_execution(client, admin_headers):
    res = client.post('/api/payroll/runs/execute', json={
        'month': 5,
        'year': 2026
    }, headers=admin_headers)

    assert res.status_code == 200
    assert res.json['run']['status'] == 'Approved'

def test_payslip_retrieval(client, admin_headers):
    res = client.get('/api/payroll/payslips', headers=admin_headers)
    assert res.status_code == 200

def test_tax_declaration_submission(client, hr_headers):
    res = client.post('/api/payroll/tax-declarations', json={
        'employee_id': 1,
        'financial_year': '2026-2027',
        'regime': 'New',
        'sec_80c_ppf_elss': 150000.0,
        'sec_80d_health_insurance': 25000.0
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['declaration']['total_declared_investments'] == 175000.0
