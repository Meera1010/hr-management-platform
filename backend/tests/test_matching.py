import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.role import Role
from app.models.user import User
from app.models.candidate import Candidate
from app.models.department import Department
from app.models.job import Job
from app.services.job_matcher import calculate_skill_match, extract_job_skills, extract_candidate_skills

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        r_cand = Role(name='Candidate', description='Candidate role')
        r_rec = Role(name='Recruiter', description='Recruiter role')
        db.session.add_all([r_cand, r_rec])
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
        r_cand = Role.query.filter_by(name='Candidate').first()
        r_rec = Role.query.filter_by(name='Recruiter').first()

        u_cand = User(first_name='Test', last_name='Cand', email='cand_match@example.com', role_id=r_cand.id)
        u_cand.set_password('pass123')

        u_rec = User(first_name='Test', last_name='Rec', email='rec_match@example.com', role_id=r_rec.id)
        u_rec.set_password('pass123')

        db.session.add_all([u_cand, u_rec])
        db.session.commit()

        dept = Department(name='Engineering', description='Tech dept')
        db.session.add(dept)
        db.session.commit()

        c = Candidate(
            candidate_code='CAND-M1',
            first_name='Test',
            last_name='Cand',
            email='cand_match@example.com',
            skills='Python, Flask, SQL',
            user_id=u_cand.id
        )
        db.session.add(c)

        job1 = Job(
            job_code='JOB-M1',
            title='Python Engineer',
            department_id=dept.id,
            description='Python job',
            required_skills='Python, Flask, SQL, Docker', # 4 skills
            status='Open'
        )

        job2 = Job(
            job_code='JOB-M2',
            title='Full Stack Developer',
            department_id=dept.id,
            description='Web job',
            required_skills='Python, Flask, SQL', # 3 skills -> 100% match
            status='Open'
        )

        job3 = Job(
            job_code='JOB-M3',
            title='Java Developer',
            department_id=dept.id,
            description='Java job',
            required_skills='Java, Spring, Microservices', # 0 matched -> 0%
            status='Open'
        )

        db.session.add_all([job1, job2, job3])
        db.session.commit()

        return {
            'cand_user_id': u_cand.id,
            'rec_user_id': u_rec.id,
            'cand_id': c.id,
            'job1_id': job1.id,
            'job2_id': job2.id,
            'job3_id': job3.id
        }

def get_token(client, email, password='pass123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.json['data']['access_token']

def test_calculate_skill_match_percentages():
    cand_skills = ['python', 'flask', 'sql']

    # 100% match
    res_100 = calculate_skill_match(cand_skills, ['python', 'flask', 'sql'])
    assert res_100['match_percentage'] == 100
    assert len(res_100['matched_skills']) == 3
    assert len(res_100['missing_skills']) == 0

    # 75% match
    res_75 = calculate_skill_match(cand_skills, ['python', 'flask', 'sql', 'docker'])
    assert res_75['match_percentage'] == 75
    assert len(res_75['matched_skills']) == 3
    assert res_75['missing_skills'] == ['docker']

    # 50% match
    res_50 = calculate_skill_match(cand_skills, ['python', 'flask', 'java', 'docker'])
    assert res_50['match_percentage'] == 50

    # 0% match
    res_0 = calculate_skill_match(cand_skills, ['java', 'spring'])
    assert res_0['match_percentage'] == 0

    # 0 required skills (no division by zero)
    res_none = calculate_skill_match(cand_skills, [])
    assert res_none['match_percentage'] == 0

def test_job_candidate_matching_api(client, test_data):
    token = get_token(client, 'cand_match@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    cand_id = test_data['cand_id']
    job2_id = test_data['job2_id']

    # Match detail
    res_match = client.get(f'/api/jobs/{job2_id}/match/{cand_id}', headers=headers)
    assert res_match.status_code == 200
    assert res_match.json['data']['match_percentage'] == 100
    assert 'python' in res_match.json['data']['matched_skills']

    # Candidate ranked matches
    res_list = client.get(f'/api/candidates/{cand_id}/matches', headers=headers)
    assert res_list.status_code == 200
    matches = res_list.json['data']
    assert len(matches) == 3
    # First match should be Full Stack Developer (100%)
    assert matches[0]['match_percentage'] == 100
    assert matches[0]['job_id'] == job2_id

def test_recruiter_job_matches_ranking_api(client, test_data):
    token = get_token(client, 'rec_match@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    job1_id = test_data['job1_id']
    res = client.get(f'/api/jobs/{job1_id}/matches', headers=headers)
    assert res.status_code == 200
    candidates = res.json['data']['candidates']
    assert len(candidates) >= 1
    assert candidates[0]['match_percentage'] == 75
