import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.role import Role
from app.models.user import User
from app.models.candidate import Candidate
from app.models.department import Department
from app.models.job import Job
from app.services.candidate_ranker import CandidateRanker

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
        r_emp = Role.query.filter_by(name='Employee').first()

        u_rec = User(first_name='Recruiter', last_name='User', email='rec_rank@example.com', role_id=r_rec.id)
        u_rec.set_password('pass123')

        u_emp = User(first_name='Emp', last_name='User', email='emp_rank@example.com', role_id=r_emp.id)
        u_emp.set_password('pass123')

        db.session.add_all([u_rec, u_emp])
        db.session.commit()

        dept = Department(name='Engineering', description='Tech')
        db.session.add(dept)
        db.session.commit()

        job = Job(
            job_code='JOB-R1',
            title='Senior Python Engineer',
            department_id=dept.id,
            description='Tech job',
            required_skills='Python, Flask, SQL',
            experience_required='5 years',
            education_required='B.Tech',
            status='Open'
        )
        db.session.add(job)
        db.session.commit()

        # Candidate 1: High match (100% skills, 5 yrs exp, B.Tech edu) -> Score 100
        u1 = User(first_name='High', last_name='Match', email='c1@example.com', role_id=r_cand.id)
        u1.set_password('pass123')
        db.session.add(u1)
        db.session.commit()
        c1 = Candidate(candidate_code='C1', first_name='High', last_name='Match', email='c1@example.com', skills='Python, Flask, SQL', experience_years=5, education='B.Tech CS', user_id=u1.id)

        # Candidate 2: Partial match (66.7% skills, 2 yrs exp, B.Tech edu)
        u2 = User(first_name='Low', last_name='Match', email='c2@example.com', role_id=r_cand.id)
        u2.set_password('pass123')
        db.session.add(u2)
        db.session.commit()
        c2 = Candidate(candidate_code='C2', first_name='Low', last_name='Match', email='c2@example.com', skills='Python, SQL', experience_years=2, education='B.Tech CS', user_id=u2.id)

        db.session.add_all([c1, c2])
        db.session.commit()

        return {
            'rec_id': u_rec.id,
            'emp_id': u_emp.id,
            'job_id': job.id,
            'c1_id': c1.id,
            'c2_id': c2.id
        }

def get_token(client, email, password='pass123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.json['data']['access_token']

def test_candidate_ranker_scoring_formula(app, test_data):
    with app.app_context():
        job = Job.query.get(test_data['job_id'])
        c1 = Candidate.query.get(test_data['c1_id'])

        rank1 = CandidateRanker.rank_candidate_for_job(c1, job)
        assert rank1['skill_score'] == 100.0
        assert rank1['experience_score'] == 100.0
        assert rank1['education_score'] == 100.0
        # (100 * 0.60) + (100 * 0.25) + (100 * 0.15) = 100.0
        assert rank1['score'] == 100.0
        assert "Strong skill alignment" in rank1['explanation']

def test_rankings_api_auth(client, test_data):
    rec_token = get_token(client, 'rec_rank@example.com')
    emp_token = get_token(client, 'emp_rank@example.com')
    job_id = test_data['job_id']

    # Recruiter gets rankings
    res_rec = client.get(f'/api/jobs/{job_id}/rank-candidates', headers={'Authorization': f'Bearer {rec_token}'})
    assert res_rec.status_code == 200
    candidates = res_rec.json['data']['candidates']
    assert len(candidates) == 2
    assert candidates[0]['score'] >= candidates[1]['score']

    # Employee denied
    res_emp = client.get(f'/api/jobs/{job_id}/rank-candidates', headers={'Authorization': f'Bearer {emp_token}'})
    assert res_emp.status_code == 403
