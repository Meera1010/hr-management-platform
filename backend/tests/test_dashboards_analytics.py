import pytest

def test_dashboard_stats(client, admin_headers, employee_headers, candidate_headers):
    # Admin dashboard stats
    res_admin = client.get('/api/dashboards/stats', headers=admin_headers)
    assert res_admin.status_code == 200
    assert 'metrics' in res_admin.get_json()['data']

    # Employee dashboard stats
    res_emp = client.get('/api/dashboards/stats', headers=employee_headers)
    assert res_emp.status_code == 200

    # Candidate dashboard stats
    res_cand = client.get('/api/dashboards/stats', headers=candidate_headers)
    assert res_cand.status_code == 200

def test_analytics_overview(client, admin_headers):
    res = client.get('/api/analytics/overview', headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'funnel' in data['analytics']

def test_reports_json_and_csv(client, admin_headers):
    # Headcount JSON
    h_res = client.get('/api/reports/headcount', headers=admin_headers)
    assert h_res.status_code == 200

    # Headcount CSV
    h_csv = client.get('/api/reports/headcount?export=csv', headers=admin_headers)
    assert h_csv.status_code == 200
    assert 'text/csv' in h_csv.content_type

    # Attendance CSV
    a_csv = client.get('/api/reports/attendance?export=csv', headers=admin_headers)
    assert a_csv.status_code == 200

def test_global_search(client, admin_headers):
    res = client.get('/api/search?q=Demo', headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'results' in data

def test_career_recommendations(client, candidate_headers, admin_headers):
    res = client.get('/api/recommendations/my-recommendations', headers=candidate_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert 'recommendations' in data
