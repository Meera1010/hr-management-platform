import pytest
from app.models.candidate import Candidate

def test_create_candidate_recruiter(client, recruiter_headers):
    response = client.post('/api/candidates', json={
        'candidate_code': 'CAN-001',
        'first_name': 'Test',
        'last_name': 'Candidate',
        'email': 'testcan@example.com',
        'experience_years': 2,
        'status': 'Available'
    }, headers=recruiter_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['candidate']['email'] == 'testcan@example.com'

def test_create_candidate_invalid_email(client, recruiter_headers):
    response = client.post('/api/candidates', json={
        'candidate_code': 'CAN-002',
        'first_name': 'Test',
        'last_name': 'Candidate',
        'email': 'invalid-email',
        'experience_years': 2
    }, headers=recruiter_headers)
    
    assert response.status_code == 400
    assert 'Invalid email format' in response.get_json()['message']

def test_create_candidate_negative_experience(client, recruiter_headers):
    response = client.post('/api/candidates', json={
        'candidate_code': 'CAN-003',
        'first_name': 'Test',
        'last_name': 'Candidate',
        'email': 'testcan3@example.com',
        'experience_years': -5
    }, headers=recruiter_headers)
    
    assert response.status_code == 400
    assert 'Experience must be zero or greater' in response.get_json()['message']

def test_create_candidate_duplicate_email(client, recruiter_headers):
    client.post('/api/candidates', json={
        'candidate_code': 'CAN-004',
        'first_name': 'Test',
        'last_name': 'Candidate',
        'email': 'dup@example.com'
    }, headers=recruiter_headers)
    
    response = client.post('/api/candidates', json={
        'candidate_code': 'CAN-005',
        'first_name': 'Test2',
        'last_name': 'Candidate2',
        'email': 'dup@example.com'
    }, headers=recruiter_headers)
    
    assert response.status_code == 400
    assert 'already exists' in response.get_json()['message']

def test_get_candidates_admin(client, admin_headers, app_context):
    from app.models.candidate import Candidate
    from app import db
    db.session.add(Candidate(candidate_code='C1', first_name='A', last_name='B', email='a@b.com'))
    db.session.commit()
    
    response = client.get('/api/candidates', headers=admin_headers)
    assert response.status_code == 200
    assert len(response.get_json()['candidates']) >= 1

def test_get_candidates_employee_denied(client, employee_headers):
    response = client.get('/api/candidates', headers=employee_headers)
    assert response.status_code == 403

def test_candidate_self_profile(client, candidate_headers):
    response = client.get('/api/candidates/me', headers=candidate_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['candidate']['email'] == 'candidate_test@example.com'

def test_candidate_update_self_profile(client, candidate_headers):
    response = client.put('/api/candidates/me', json={
        'first_name': 'UpdatedName',
        'status': 'Hired' # Should be ignored
    }, headers=candidate_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['candidate']['first_name'] == 'UpdatedName'
    assert data['candidate']['status'] == 'Available' # Unchanged

def test_search_and_filter(client, recruiter_headers, app_context):
    from app.models.candidate import Candidate
    from app import db
    db.session.add(Candidate(candidate_code='S1', first_name='John', last_name='Doe', email='j@d.com', experience_years=5, status='Hired', skills='Python, Java'))
    db.session.add(Candidate(candidate_code='S2', first_name='Jane', last_name='Smith', email='j@s.com', experience_years=2, status='Available', skills='React'))
    db.session.commit()
    
    # Search
    response = client.get('/api/candidates?search=John', headers=recruiter_headers)
    data = response.get_json()
    assert len(data['candidates']) == 1
    assert data['candidates'][0]['first_name'] == 'John'
    
    # Filter by experience
    response = client.get('/api/candidates?experience_years=4', headers=recruiter_headers)
    data = response.get_json()
    assert len(data['candidates']) == 1
    assert data['candidates'][0]['experience_years'] == 5
    
    # Filter by status
    response = client.get('/api/candidates?status=Available', headers=recruiter_headers)
    data = response.get_json()
    # Depending on what's in the DB from other tests, there might be more, but at least Jane
    assert any(c['first_name'] == 'Jane' for c in data['candidates'])
