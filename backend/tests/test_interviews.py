import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.role import Role
from app.models.user import User
from app.models.candidate import Candidate
from app.models.department import Department
from app.models.job import Job
from app.models.application import Application
from app.models.interview import Interview

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        r_cand = Role(name='Candidate', description='Candidate role')
        r_rec = Role(name='Recruiter', description='Recruiter role')
        r_emp = Role(name='Employee', description='Employee role')
        db.session.add_all([r_cand, r_rec, r_emp])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_data(app):
    with app.app_context():
        r_rec = Role.query.filter_by(name='Recruiter').first()
        r_cand = Role.query.filter_by(name='Candidate').first()

        u_rec = User(first_name='Recruiter', last_name='User', email='rec_int@example.com', role_id=r_rec.id)
        u_rec.set_password('pass123')

        u_cand = User(first_name='Candidate', last_name='User', email='cand_int@example.com', role_id=r_cand.id)
        u_cand.set_password('pass123')

        db.session.add_all([u_rec, u_cand])
        db.session.commit()

        dept = Department(name='Engineering', description='Tech')
        db.session.add(dept)
        db.session.commit()

        job = Job(job_code='JOB-I1', title='Software Engineer', department_id=dept.id, description='Tech job', status='Open')
        db.session.add(job)

        cand = Candidate(candidate_code='CAND-I1', first_name='Candidate', last_name='User', email='cand_int@example.com', user_id=u_cand.id)
        db.session.add(cand)
        db.session.commit()

        appl = Application(application_code='APP-I1', candidate_id=cand.id, job_id=job.id, status='Shortlisted')
        db.session.add(appl)
        db.session.commit()

        return {
            'rec_id': u_rec.id,
            'cand_id': u_cand.id,
            'app_id': appl.id
        }

def get_token(client, email, password='pass123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.json['data']['access_token']

def test_create_interview_success_and_conflict(client, test_data):
    token = get_token(client, 'rec_int@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'application_id': test_data['app_id'],
        'interviewer_name': 'Sarah Lead',
        'interview_type': 'Technical',
        'scheduled_date': '2026-09-10',
        'scheduled_time': '10:00',
        'duration_minutes': 45
    }

    # 1. Successful scheduling
    res = client.post('/api/interviews', json=payload, headers=headers)
    assert res.status_code == 201
    assert res.json['success'] is True
    assert res.json['data']['interview_code'].startswith('INT-')

    # 2. Scheduling Conflict test (same interviewer, date, and time)
    res_conflict = client.post('/api/interviews', json=payload, headers=headers)
    assert res_conflict.status_code == 400
    assert "Interviewer already has an interview at this time" in res_conflict.json['message']

def test_interview_feedback_submission(client, test_data):
    token = get_token(client, 'rec_int@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    # Create interview
    res_int = client.post('/api/interviews', json={
        'application_id': test_data['app_id'],
        'interviewer_name': 'David Manager',
        'interview_type': 'HR',
        'scheduled_date': '2026-09-12',
        'scheduled_time': '14:00'
    }, headers=headers)
    int_id = res_int.json['data']['id']

    # Submit feedback (Technical: 4, Comm: 5, Problem: 3 -> overall = 4.0)
    fb_payload = {
        'technical_score': 4,
        'communication_score': 5,
        'problem_solving_score': 3,
        'recommendation': 'Recommend',
        'comments': 'Great communication skills.'
    }

    res_fb = client.post(f'/api/interviews/{int_id}/feedback', json=fb_payload, headers=headers)
    assert res_fb.status_code == 201
    assert res_fb.json['data']['overall_score'] == 4.0
    assert res_fb.json['data']['recommendation'] == 'Recommend'

    # Verify interview status became Completed
    res_get = client.get(f'/api/interviews/{int_id}', headers=headers)
    assert res_get.json['data']['status'] == 'Completed'
