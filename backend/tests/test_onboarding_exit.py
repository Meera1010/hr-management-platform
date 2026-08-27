import pytest

def test_initiate_onboarding_plan(client, hr_headers):
    res = client.post('/api/lifecycle/onboarding/checklists/initiate', json={
        'employee_id': 1
    }, headers=hr_headers)

    assert res.status_code == 201
    assert len(res.json['checklist']['tasks']) == 6

def test_toggle_onboarding_task(client, hr_headers):
    init_res = client.post('/api/lifecycle/onboarding/checklists/initiate', json={'employee_id': 1}, headers=hr_headers)
    task_id = init_res.json['checklist']['tasks'][0]['id']

    toggle_res = client.post(f'/api/lifecycle/onboarding/tasks/{task_id}/toggle', headers=hr_headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json['task']['is_completed'] is True

def test_submit_resignation_and_clearance(client, hr_headers):
    res = client.post('/api/lifecycle/resignations', json={
        'employee_id': 1,
        'reason': 'Pursuing higher studies abroad.',
        'requested_last_working_day': '2026-08-31',
        'notice_period_days': 60
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['resignation']['status'] == 'Submitted'
    resignation_id = res.json['resignation']['id']

    # Update clearance
    clear_res = client.post(f'/api/lifecycle/resignations/{resignation_id}/clearance', json={
        'department_name': 'IT',
        'status': 'Cleared',
        'remarks': 'Laptop AST-M3-001 returned in excellent condition.'
    }, headers=hr_headers)

    assert clear_res.status_code == 200
    assert clear_res.json['clearance']['status'] == 'Cleared'

def test_fnf_settlement_calculation(client, admin_headers):
    res_sub = client.post('/api/lifecycle/resignations', json={
        'employee_id': 1,
        'reason': 'Relocating to another city.',
        'requested_last_working_day': '2026-09-15'
    }, headers=admin_headers)
    res_id = res_sub.json['resignation']['id']

    fnf_res = client.post('/api/lifecycle/fnf-settlements/calculate', json={
        'resignation_request_id': res_id,
        'unpaid_salary_amount': 50000.0,
        'leave_encashment_amount': 15000.0,
        'gratuity_amount': 70000.0
    }, headers=admin_headers)

    assert fnf_res.status_code == 200
    assert fnf_res.json['settlement']['net_settlement_amount'] == 135000.0
