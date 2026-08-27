"""
Tests for Performance Review module — Step 10
Uses fictional demo data. No real personal information.
"""
import pytest
from datetime import date
from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.models.performance_review import PerformanceReview


@pytest.fixture
def app():
    from app.config import Config

    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        JWT_SECRET_KEY = 'test-secret-performance'

    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
    with application.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_data(app):
    with app.app_context():
        emp_role = Role(name='Employee', description='Employee')
        hr_role = Role(name='HR', description='HR')
        rec_role = Role(name='Recruiter', description='Recruiter')
        db.session.add_all([emp_role, hr_role, rec_role])
        db.session.commit()

        dept = Department(name='Engineering', description='Eng', status='Active')
        db.session.add(dept)
        db.session.commit()

        emp_user = User(first_name='Casey', last_name='Jones', email='casey@example.com', role_id=emp_role.id)
        emp_user.set_password('testpass123')
        hr_user = User(first_name='HR', last_name='Mgr', email='hr@example.com', role_id=hr_role.id)
        hr_user.set_password('testpass123')
        rec_user = User(first_name='Recruiter', last_name='Demo', email='rec@example.com', role_id=rec_role.id)
        rec_user.set_password('testpass123')
        db.session.add_all([emp_user, hr_user, rec_user])
        db.session.commit()

        emp = Employee(
            employee_code='CASE001', first_name='Casey', last_name='Jones',
            email='casey.emp@example.com', department_id=dept.id, user_id=emp_user.id,
            designation='Engineer', joining_date=date(2024, 1, 1), employment_type='Full Time', status='Active'
        )
        db.session.add(emp)
        db.session.commit()

        return {
            'emp_email': 'casey@example.com',
            'hr_email': 'hr@example.com',
            'rec_email': 'rec@example.com',
            'employee_id': emp.id,
        }


def _login(client, email, password='testpass123'):
    resp = client.post('/api/auth/login', json={'email': email, 'password': password})
    return resp.get_json()['data']['access_token']


def _create_review(client, token, employee_id, status='Completed'):
    return client.post(
        '/api/performance',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'employee_id': employee_id,
            'review_period': 'Q3 2026',
            'productivity_score': 4,
            'quality_score': 5,
            'teamwork_score': 4,
            'goal_score': 3,
            'reviewer_name': 'Morgan Davis',
            'comments': 'Good performer overall.',
            'status': status
        }
    )


# ─── Test 1: HR Can Create Performance Review ─────────────────────────────────

def test_hr_create_performance_review(client, test_data):
    hr_token = _login(client, test_data['hr_email'])
    resp = _create_review(client, hr_token, test_data['employee_id'])
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['data']['overall_score'] == 4.0
    assert data['data']['status'] == 'Completed'


# ─── Test 2: Score Validation (1–5 Only) ──────────────────────────────────────

def test_score_validation(client, test_data):
    hr_token = _login(client, test_data['hr_email'])
    # Score of 6 should fail
    resp = client.post(
        '/api/performance',
        headers={'Authorization': f'Bearer {hr_token}'},
        json={
            'employee_id': test_data['employee_id'],
            'review_period': 'Q3 2026',
            'productivity_score': 6,
            'quality_score': 5,
            'teamwork_score': 4,
            'goal_score': 3,
            'reviewer_name': 'Morgan Davis',
            'status': 'Draft'
        }
    )
    data = resp.get_json()
    assert resp.status_code == 400
    assert data['success'] is False
    assert 'productivity_score' in data['message'].lower() or '1 and 5' in data['message']


# ─── Test 3: Overall Score Calculation ────────────────────────────────────────

def test_overall_score_calculation():
    # 4 + 5 + 4 + 3 = 16 / 4 = 4.0
    assert PerformanceReview.compute_overall(4, 5, 4, 3) == 4.0
    # 5 + 5 + 5 + 5 = 20 / 4 = 5.0
    assert PerformanceReview.compute_overall(5, 5, 5, 5) == 5.0
    # 1 + 1 + 1 + 1 = 4 / 4 = 1.0
    assert PerformanceReview.compute_overall(1, 1, 1, 1) == 1.0
    # 4 + 5 + 4 + 5 = 18 / 4 = 4.5
    assert PerformanceReview.compute_overall(4, 5, 4, 5) == 4.5


# ─── Test 4: HR Can Update Review ────────────────────────────────────────────

def test_hr_update_review(client, test_data):
    hr_token = _login(client, test_data['hr_email'])
    create_resp = _create_review(client, hr_token, test_data['employee_id'], status='Draft')
    review_id = create_resp.get_json()['data']['id']

    resp = client.put(
        f'/api/performance/{review_id}',
        headers={'Authorization': f'Bearer {hr_token}'},
        json={'status': 'Completed', 'comments': 'Finalized after review discussion.'}
    )
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['data']['status'] == 'Completed'
    assert data['data']['comments'] == 'Finalized after review discussion.'


# ─── Test 5: Employee Sees Only Own Completed Reviews ─────────────────────────

def test_employee_sees_only_own_completed_reviews(client, app, test_data):
    hr_token = _login(client, test_data['hr_email'])
    # Create completed review for employee
    _create_review(client, hr_token, test_data['employee_id'], status='Completed')

    emp_token = _login(client, test_data['emp_email'])
    resp = client.get('/api/performance', headers={'Authorization': f'Bearer {emp_token}'})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    # All returned reviews must be Completed
    for review in data['data']:
        assert review['status'] == 'Completed'
        assert review['employee_id'] == test_data['employee_id']


# ─── Test 6: Unauthorized Role Cannot Access Performance ──────────────────────

def test_recruiter_cannot_access_performance(client, test_data):
    rec_token = _login(client, test_data['rec_email'])
    resp = client.get('/api/performance', headers={'Authorization': f'Bearer {rec_token}'})
    data = resp.get_json()
    assert resp.status_code == 403
    assert data['success'] is False
