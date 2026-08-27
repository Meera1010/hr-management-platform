import pytest

def test_objective_creation_and_kr_progress(client, hr_headers):
    res = client.post('/api/okrs/objectives', json={
        'title': 'Achieve 99.9% Platform Uptime',
        'level': 'Department',
        'period_quarter': '2026-Q2',
        'start_date': '2026-04-01',
        'end_date': '2026-06-30'
    }, headers=hr_headers)

    assert res.status_code == 201
    obj_id = res.json['objective']['id']

    # Add Key Result
    kr_res = client.post(f'/api/okrs/objectives/{obj_id}/key-results', json={
        'title': 'Deploy multi-region cloud failover cluster',
        'target_value': 100.0,
        'current_value': 0.0,
        'unit': '%'
    }, headers=hr_headers)

    assert kr_res.status_code == 201
    kr_id = kr_res.json['key_result']['id']

    # Update KR progress
    upd_res = client.post(f'/api/okrs/key-results/{kr_id}/update-progress', json={
        'current_value': 80.0
    }, headers=hr_headers)

    assert upd_res.status_code == 200
    assert upd_res.json['key_result']['progress_pct'] == 80.0

def test_get_review_cycles_and_feedback(client, hr_headers):
    res_c = client.get('/api/okrs/review-cycles', headers=hr_headers)
    assert res_c.status_code == 200

    res_f = client.get('/api/okrs/360-feedback', headers=hr_headers)
    assert res_f.status_code == 200
