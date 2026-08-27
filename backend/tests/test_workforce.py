import pytest
from app import db
from app.models.employee import Employee
from app.models.department import Department
from datetime import date

def test_workforce_plans_and_benchmarks(client, admin_headers):
    p_res = client.get('/api/workforce/plans', headers=admin_headers)
    assert p_res.status_code == 200

    b_res = client.get('/api/workforce/benchmarks', headers=admin_headers)
    assert b_res.status_code == 200

def test_attrition_risk_evaluation(client, admin_headers, app_context):
    # Ensure a department and employee exist first
    dept = Department(name='Analytics', description='Analytics Dept')
    db.session.add(dept)
    db.session.commit()

    emp = Employee(
        employee_code='EMP-RISK-01',
        first_name='Test',
        last_name='Risk',
        email='risk_test@example.com',
        department_id=dept.id,
        designation='Data Analyst',
        joining_date=date(2022, 1, 1),
        employment_type='Full Time'
    )
    db.session.add(emp)
    db.session.commit()

    res = client.post(f'/api/workforce/evaluate-attrition/{emp.id}', headers=admin_headers)
    assert res.status_code == 200
    assert 'risk_level' in res.json['risk']
