import pytest

def test_grievance_submission(client, hr_headers):
    res = client.post('/api/compliance/grievances', json={
        'subject': 'Unclear Project Deadline Allocation',
        'description': 'Sprint deadlines communicated without backlog review.',
        'category': 'Workplace Conduct',
        'severity': 'Low',
        'is_anonymous': False
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['ticket']['status'] == 'Open'

def test_policies_and_audit_logs(client, admin_headers):
    p_res = client.get('/api/compliance/policies', headers=admin_headers)
    assert p_res.status_code == 200

    a_res = client.get('/api/compliance/audit-logs', headers=admin_headers)
    assert a_res.status_code == 200
