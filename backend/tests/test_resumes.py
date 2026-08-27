import os
import io
import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.role import Role
from app.models.user import User
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.skill import Skill
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        # Seed basic roles
        r_cand = Role(name='Candidate', description='Candidate role')
        r_rec = Role(name='Recruiter', description='Recruiter role')
        r_emp = Role(name='Employee', description='Employee role')
        db.session.add_all([r_cand, r_rec, r_emp])
        db.session.commit()

        # Seed Skills
        s1 = Skill(name='Python', category='Programming')
        s2 = Skill(name='SQL', category='Database')
        s3 = Skill(name='Flask', category='Web Development')
        db.session.add_all([s1, s2, s3])
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
        r_emp = Role.query.filter_by(name='Employee').first()

        u_cand1 = User(first_name='Candidate', last_name='One', email='cand1@example.com', role_id=r_cand.id)
        u_cand1.set_password('pass123')

        u_cand2 = User(first_name='Candidate', last_name='Two', email='cand2@example.com', role_id=r_cand.id)
        u_cand2.set_password('pass123')

        u_rec = User(first_name='Recruiter', last_name='User', email='recruiter@example.com', role_id=r_rec.id)
        u_rec.set_password('pass123')

        u_emp = User(first_name='Employee', last_name='User', email='employee@example.com', role_id=r_emp.id)
        u_emp.set_password('pass123')

        db.session.add_all([u_cand1, u_cand2, u_rec, u_emp])
        db.session.commit()

        c1 = Candidate(candidate_code='CAND-001', first_name='Candidate', last_name='One', email='cand1@example.com', user_id=u_cand1.id)
        c2 = Candidate(candidate_code='CAND-002', first_name='Candidate', last_name='Two', email='cand2@example.com', user_id=u_cand2.id)
        db.session.add_all([c1, c2])
        db.session.commit()

        return {
            'cand1_user_id': u_cand1.id,
            'cand2_user_id': u_cand2.id,
            'rec_user_id': u_rec.id,
            'emp_user_id': u_emp.id,
            'cand1_id': c1.id,
            'cand2_id': c2.id
        }

def get_token(client, email, password='pass123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.json['data']['access_token']

def test_resume_parser_txt(tmp_path):
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Experienced Python and SQL developer with Flask background.", encoding="utf-8")

    res = ResumeParser.extract_text(str(txt_file), 'TXT')
    assert res['success'] is True
    assert "Python" in res['text']

def test_skill_extractor():
    text = "I have experience in Python, Flask, and SQL databases."
    skills = SkillExtractor.extract_skills(text, ['Python', 'Flask', 'SQL', 'Java', 'Docker'])
    assert 'Python' in skills
    assert 'Flask' in skills
    assert 'SQL' in skills
    assert 'Java' not in skills
    assert 'Docker' not in skills

def test_upload_resume_success(client, test_data):
    token = get_token(client, 'cand1@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    file_content = b"Candidate Resume\nSkills: Python, Flask, SQL"
    data = {
        'file': (io.BytesIO(file_content), 'my_resume.txt')
    }

    res = client.post('/api/resumes/upload', data=data, headers=headers, content_type='multipart/form-data')
    assert res.status_code == 201
    assert res.json['success'] is True
    assert res.json['data']['resume_code'].startswith('RES-')
    assert 'Python' in res.json['data']['extracted_skills']

def test_upload_resume_invalid_extension(client, test_data):
    token = get_token(client, 'cand1@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    data = {
        'file': (io.BytesIO(b"echo 'malicious'"), 'script.exe')
    }

    res = client.post('/api/resumes/upload', data=data, headers=headers, content_type='multipart/form-data')
    assert res.status_code == 400
    assert res.json['success'] is False
    assert "Invalid file extension" in res.json['message']

def test_resume_ownership_and_auth(client, test_data):
    token1 = get_token(client, 'cand1@example.com')
    token2 = get_token(client, 'cand2@example.com')
    emp_token = get_token(client, 'employee@example.com')

    # Upload for Candidate 1
    res = client.post('/api/resumes/upload', data={'file': (io.BytesIO(b"Resume text Python"), 'res1.txt')},
                      headers={'Authorization': f'Bearer {token1}'}, content_type='multipart/form-data')
    resume_id = res.json['data']['id']

    # Candidate 2 trying to get Candidate 1's resume -> 403
    res_get2 = client.get(f'/api/resumes/{resume_id}', headers={'Authorization': f'Bearer {token2}'})
    assert res_get2.status_code == 403

    # Employee trying to access resumes -> 403
    res_emp = client.get('/api/resumes', headers={'Authorization': f'Bearer {emp_token}'})
    assert res_emp.status_code == 403

    # Candidate 1 can retrieve own resume
    res_get1 = client.get(f'/api/resumes/{resume_id}', headers={'Authorization': f'Bearer {token1}'})
    assert res_get1.status_code == 200
    assert res_get1.json['data']['id'] == resume_id

def test_delete_and_download_resume(client, test_data):
    token = get_token(client, 'cand1@example.com')
    headers = {'Authorization': f'Bearer {token}'}

    # Upload
    res = client.post('/api/resumes/upload', data={'file': (io.BytesIO(b"Resume download test text"), 'download_test.txt')},
                      headers=headers, content_type='multipart/form-data')
    resume_id = res.json['data']['id']

    # Download
    res_dl = client.get(f'/api/resumes/{resume_id}/download', headers=headers)
    assert res_dl.status_code == 200
    assert b"Resume download test text" in res_dl.data

    # Delete
    res_del = client.delete(f'/api/resumes/{resume_id}', headers=headers)
    assert res_del.status_code == 200
    assert res_del.json['success'] is True
