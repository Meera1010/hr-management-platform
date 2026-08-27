import pytest
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.models.candidate import Candidate
from app.models.department import Department
from app.models.job import Job
from app.models.application import Application
from flask_jwt_extended import create_access_token
import json

@pytest.fixture
def app():
    app = create_app('app.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_roles_and_users(app):
    with app.app_context():
        roles = {
            'Admin': Role(name='Admin', description='System Administrator'),
            'HR': Role(name='HR', description='Human Resources'),
            'Recruiter': Role(name='Recruiter', description='Recruiter'),
            'Candidate': Role(name='Candidate', description='Job Applicant')
        }
        for role in roles.values():
            db.session.add(role)
        db.session.commit()

        # Users
        users = {
            'admin': User(first_name='Admin', last_name='User', email='admin@example.com', role_id=roles['Admin'].id),
            'hr': User(first_name='HR', last_name='User', email='hr@example.com', role_id=roles['HR'].id),
            'recruiter': User(first_name='Recruiter', last_name='User', email='recruiter@example.com', role_id=roles['Recruiter'].id),
            'candidate1': User(first_name='Candidate1', last_name='User', email='c1@example.com', role_id=roles['Candidate'].id),
            'candidate2': User(first_name='Candidate2', last_name='User', email='c2@example.com', role_id=roles['Candidate'].id)
        }
        for u in users.values():
            u.set_password('password123')
            db.session.add(u)
        db.session.commit()

        # Candidate Profiles
        c1 = Candidate(user_id=users['candidate1'].id, candidate_code='CAN-T01', first_name='C1', last_name='U', email='c1@example.com', phone='111', status='Active')
        c2 = Candidate(user_id=users['candidate2'].id, candidate_code='CAN-T02', first_name='C2', last_name='U', email='c2@example.com', phone='222', status='Active')
        db.session.add_all([c1, c2])
        
        # Dept & Job
        dept = Department(name='Engineering', description='Eng Dept')
        db.session.add(dept)
        db.session.commit()
        
        job_open = Job(job_code='J-01', title='Dev', department_id=dept.id, description='Desc', status='Open', created_by=users['recruiter'].id)
        job_closed = Job(job_code='J-02', title='Dev2', department_id=dept.id, description='Desc2', status='Closed', created_by=users['recruiter'].id)
        db.session.add_all([job_open, job_closed])
        db.session.commit()

        return {
            'roles': {k: v.id for k, v in roles.items()},
            'users': {k: v.id for k, v in users.items()},
            'jobs': {'open': job_open.id, 'closed': job_closed.id},
            'candidates': {'c1': c1.id, 'c2': c2.id}
        }

def get_token(user_id):
    return create_access_token(identity=str(user_id))

def test_create_application(client, setup_roles_and_users):
    token = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    
    response = client.post('/api/applications',
                           headers={'Authorization': f'Bearer {token}'},
                           json={'job_id': job_id, 'cover_letter': 'Hello!'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['application']['status'] == 'Submitted'
    assert data['application']['application_code'] == 'APP-0001'

def test_create_application_duplicate(client, setup_roles_and_users):
    token = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    
    client.post('/api/applications', headers={'Authorization': f'Bearer {token}'}, json={'job_id': job_id})
    
    # Second time
    response = client.post('/api/applications', headers={'Authorization': f'Bearer {token}'}, json={'job_id': job_id})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'You have already applied for this job'

def test_create_application_closed_job(client, setup_roles_and_users):
    token = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['closed']
    
    response = client.post('/api/applications', headers={'Authorization': f'Bearer {token}'}, json={'job_id': job_id})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'not open' in data['message']

def test_get_applications_recruiter(client, setup_roles_and_users):
    token_c1 = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    client.post('/api/applications', headers={'Authorization': f'Bearer {token_c1}'}, json={'job_id': job_id})
    
    token_recruiter = get_token(setup_roles_and_users['users']['recruiter'])
    response = client.get('/api/applications', headers={'Authorization': f'Bearer {token_recruiter}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_records'] == 1

def test_get_applications_candidate_only_sees_own(client, setup_roles_and_users):
    token_c1 = get_token(setup_roles_and_users['users']['candidate1'])
    token_c2 = get_token(setup_roles_and_users['users']['candidate2'])
    job_id = setup_roles_and_users['jobs']['open']
    
    client.post('/api/applications', headers={'Authorization': f'Bearer {token_c1}'}, json={'job_id': job_id})
    
    response = client.get('/api/applications', headers={'Authorization': f'Bearer {token_c2}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_records'] == 0
    
    response2 = client.get('/api/applications', headers={'Authorization': f'Bearer {token_c1}'})
    data2 = json.loads(response2.data)
    assert data2['total_records'] == 1

def test_update_status_recruiter(client, setup_roles_and_users):
    token_c1 = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    res = client.post('/api/applications', headers={'Authorization': f'Bearer {token_c1}'}, json={'job_id': job_id})
    app_id = json.loads(res.data)['application']['id']
    
    token_recruiter = get_token(setup_roles_and_users['users']['recruiter'])
    response = client.patch(f'/api/applications/{app_id}/status',
                            headers={'Authorization': f'Bearer {token_recruiter}'},
                            json={'status': 'Shortlisted', 'recruiter_notes': 'Good!'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['application']['status'] == 'Shortlisted'
    assert data['application']['recruiter_notes'] == 'Good!'

def test_update_status_candidate_forbidden(client, setup_roles_and_users):
    token_c1 = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    res = client.post('/api/applications', headers={'Authorization': f'Bearer {token_c1}'}, json={'job_id': job_id})
    app_id = json.loads(res.data)['application']['id']
    
    response = client.patch(f'/api/applications/{app_id}/status',
                            headers={'Authorization': f'Bearer {token_c1}'},
                            json={'status': 'Shortlisted'})
    assert response.status_code == 403

def test_withdraw_application(client, setup_roles_and_users):
    token_c1 = get_token(setup_roles_and_users['users']['candidate1'])
    job_id = setup_roles_and_users['jobs']['open']
    res = client.post('/api/applications', headers={'Authorization': f'Bearer {token_c1}'}, json={'job_id': job_id})
    app_id = json.loads(res.data)['application']['id']
    
    response = client.delete(f'/api/applications/{app_id}', headers={'Authorization': f'Bearer {token_c1}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['application']['status'] == 'Withdrawn'
