import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.role import Role
from app.models.user import User
from app.models.candidate import Candidate
from app.models.department import Department
from app.models.job import Job
from app.models.application import Application
from app.models.offer import Offer

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        r_cand = Role(name='Candidate', description='Candidate role')
        r_hr = Role(name='HR', description='HR role')
        r_rec = Role(name='Recruiter', description='Recruiter role')
        db.session.add_all([r_cand, r_hr, r_rec])
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
        r_hr = Role.query.filter_by(name='HR').first()
        r_cand = Role.query.filter_by(name='Candidate').first()
        r_rec = Role.query.filter_by(name='Recruiter').first()

        u_hr = User(first_name='HR', last_name='User', email='hr_off@example.com', role_id=r_hr.id)
        u_hr.set_password('pass123')

        u_cand = User(first_name='Candidate', last_name='User', email='cand_off@example.com', role_id=r_cand.id)
        u_cand.set_password('pass123')

        u_rec = User(first_name='Recruiter', last_name='User', email='rec_off@example.com', role_id=r_rec.id)
        u_rec.set_password('pass123')

        db.session.add_all([u_hr, u_cand, u_rec])
        db.session.commit()

        dept = Department(name='Engineering', description='Tech')
        db.session.add(dept)
        db.session.commit()

        job = Job(job_code='JOB-O1', title='Frontend Developer', department_id=dept.id, description='Frontend job', status='Open')
        db.session.add(job)

        cand = Candidate(candidate_code='CAND-O1', first_name='Candidate', last_name='User', email='cand_off@example.com', user_id=u_cand.id)
        db.session.add(cand)
        db.session.commit()

        appl = Application(application_code='APP-O1', candidate_id=cand.id, job_id=job.id, status='Selected')
        db.session.add(appl)
        db.session.commit()

        return {
            'hr_id': u_hr.id,
            'cand_id': u_cand.id,
            'rec_id': u_rec.id,
            'app_id': appl.id
        }

def get_token(client, email, password='pass123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.json['data']['access_token']

def test_offer_creation_and_date_validation(client, test_data):
    hr_token = get_token(client, 'hr_off@example.com')
    rec_token = get_token(client, 'rec_off@example.com')

    # Recruiter cannot create offer -> 403
    res_rec = client.post('/api/offers', json={'application_id': test_data['app_id'], 'job_title': 'Dev'}, headers={'Authorization': f'Bearer {rec_token}'})
    assert res_rec.status_code == 403

    # Invalid dates (expiration < start)
    res_invalid = client.post('/api/offers', json={
        'application_id': test_data['app_id'],
        'job_title': 'Frontend Developer',
        'offered_salary': '$90,000 / year',
        'start_date': '2026-10-15',
        'expiration_date': '2026-10-01'
    }, headers={'Authorization': f'Bearer {hr_token}'})
    assert res_invalid.status_code == 400
    assert "Expiration date cannot be earlier than start date" in res_invalid.json['message']

    # Valid creation
    res_valid = client.post('/api/offers', json={
        'application_id': test_data['app_id'],
        'job_title': 'Frontend Developer',
        'offered_salary': '$90,000 / year',
        'start_date': '2026-10-01',
        'expiration_date': '2026-10-15',
        'status': 'Draft'
    }, headers={'Authorization': f'Bearer {hr_token}'})
    assert res_valid.status_code == 201
    assert res_valid.json['data']['offer_code'].startswith('OFF-')

def test_candidate_accept_offer_workflow(client, test_data):
    hr_token = get_token(client, 'hr_off@example.com')
    cand_token = get_token(client, 'cand_off@example.com')

    # HR creates and sends offer
    res_create = client.post('/api/offers', json={
        'application_id': test_data['app_id'],
        'job_title': 'Frontend Developer',
        'offered_salary': '$90,000 / year',
        'start_date': '2026-10-01',
        'expiration_date': '2026-10-15',
        'status': 'Sent'
    }, headers={'Authorization': f'Bearer {hr_token}'})
    offer_id = res_create.json['data']['id']

    # Candidate accepts offer
    res_accept = client.post(f'/api/offers/{offer_id}/accept', headers={'Authorization': f'Bearer {cand_token}'})
    assert res_accept.status_code == 200
    assert res_accept.json['data']['status'] == 'Accepted'
