"""
Tests for Leave Management module — Step 10
Uses fictional demo data. No real personal information.
"""
import pytest
from datetime import date
from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest


@pytest.fixture
def app():
    from app.config import Config

    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        JWT_SECRET_KEY = 'test-secret-leaves'

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
        db.session.add_all([emp_role, hr_role])
        db.session.commit()

        dept = Department(name='Engineering', description='Eng', status='Active')
        db.session.add(dept)
        db.session.commit()

        emp_user = User(first_name='Jordan', last_name='Smith', email='jordan@example.com', role_id=emp_role.id)
        emp_user.set_password('testpass123')
        emp_user2 = User(first_name='Taylor', last_name='Wilson', email='taylor@example.com', role_id=emp_role.id)
        emp_user2.set_password('testpass123')
        hr_user = User(first_name='HR', last_name='Manager', email='hr@example.com', role_id=hr_role.id)
        hr_user.set_password('testpass123')
        db.session.add_all([emp_user, emp_user2, hr_user])
        db.session.commit()

        emp = Employee(
            employee_code='JORD001', first_name='Jordan', last_name='Smith',
            email='jordan.emp@example.com', department_id=dept.id, user_id=emp_user.id,
            designation='Engineer', joining_date=date(2024, 1, 1), employment_type='Full Time', status='Active'
        )
        emp2 = Employee(
            employee_code='TAYL002', first_name='Taylor', last_name='Wilson',
            email='taylor.emp@example.com', department_id=dept.id, user_id=emp_user2.id,
            designation='Analyst', joining_date=date(2024, 1, 1), employment_type='Full Time', status='Active'
        )
        db.session.add_all([emp, emp2])
        db.session.commit()

        return {
            'emp_email': 'jordan@example.com',
            'emp2_email': 'taylor@example.com',
            'hr_email': 'hr@example.com',
            'employee_id': emp.id,
            'employee2_id': emp2.id,
        }


def _login(client, email, password='testpass123'):
    resp = client.post('/api/auth/login', json={'email': email, 'password': password})
    return resp.get_json()['data']['access_token']


# ─── Test 1: Employee Can Create Leave Request ────────────────────────────────

def test_create_leave_request(client, test_data):
    token = _login(client, test_data['emp_email'])
    resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'leave_type': 'Casual',
            'start_date': '2026-09-15',
            'end_date': '2026-09-16',
            'reason': 'Personal appointment'
        }
    )
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['data']['status'] == 'Pending'
    assert data['data']['leave_type'] == 'Casual'
    assert data['data']['days_count'] == 2


# ─── Test 2: Invalid Dates Are Rejected ──────────────────────────────────────

def test_invalid_dates_rejected(client, test_data):
    token = _login(client, test_data['emp_email'])
    # end_date before start_date
    resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'leave_type': 'Annual',
            'start_date': '2026-09-20',
            'end_date': '2026-09-10',
            'reason': 'Test invalid dates'
        }
    )
    data = resp.get_json()
    assert resp.status_code == 400
    assert data['success'] is False
    assert 'end_date' in data['message'].lower() or 'before' in data['message'].lower()


# ─── Test 3: HR Can Approve Leave ────────────────────────────────────────────

def test_hr_approve_leave(client, test_data):
    emp_token = _login(client, test_data['emp_email'])
    # Create leave
    create_resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {emp_token}'},
        json={'leave_type': 'Casual', 'start_date': '2026-10-01', 'end_date': '2026-10-02', 'reason': 'Rest'}
    )
    leave_id = create_resp.get_json()['data']['id']

    hr_token = _login(client, test_data['hr_email'])
    resp = client.patch(
        f'/api/leaves/{leave_id}/approve',
        headers={'Authorization': f'Bearer {hr_token}'},
        json={'manager_comment': 'Approved. Enjoy your time.'}
    )
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert data['data']['status'] == 'Approved'


# ─── Test 4: HR Can Reject Leave ─────────────────────────────────────────────

def test_hr_reject_leave(client, test_data):
    emp_token = _login(client, test_data['emp_email'])
    create_resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {emp_token}'},
        json={'leave_type': 'Unpaid', 'start_date': '2026-10-05', 'end_date': '2026-10-06', 'reason': 'Personal'}
    )
    leave_id = create_resp.get_json()['data']['id']

    hr_token = _login(client, test_data['hr_email'])
    resp = client.patch(
        f'/api/leaves/{leave_id}/reject',
        headers={'Authorization': f'Bearer {hr_token}'},
        json={'manager_comment': 'Rejected due to project deadline.'}
    )
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['data']['status'] == 'Rejected'


# ─── Test 5: Employee Can Cancel Own Pending Leave ────────────────────────────

def test_employee_cancel_own_leave(client, test_data):
    emp_token = _login(client, test_data['emp_email'])
    create_resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {emp_token}'},
        json={'leave_type': 'Personal', 'start_date': '2026-10-10', 'end_date': '2026-10-10', 'reason': 'Personal'}
    )
    leave_id = create_resp.get_json()['data']['id']

    resp = client.patch(
        f'/api/leaves/{leave_id}/cancel',
        headers={'Authorization': f'Bearer {emp_token}'}
    )
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['data']['status'] == 'Cancelled'


# ─── Test 6: Employee Cannot Approve Leave ────────────────────────────────────

def test_employee_cannot_approve_leave(client, test_data):
    emp_token = _login(client, test_data['emp_email'])
    create_resp = client.post(
        '/api/leaves',
        headers={'Authorization': f'Bearer {emp_token}'},
        json={'leave_type': 'Casual', 'start_date': '2026-11-01', 'end_date': '2026-11-01', 'reason': 'Test'}
    )
    leave_id = create_resp.get_json()['data']['id']

    # Employee tries to approve — should be forbidden
    resp = client.patch(
        f'/api/leaves/{leave_id}/approve',
        headers={'Authorization': f'Bearer {emp_token}'}
    )
    assert resp.status_code == 403


# ─── Test 7: Employee Cannot Access Another Employee's Leaves ─────────────────

def test_employee_cannot_view_other_employee_leaves(client, app, test_data):
    with app.app_context():
        # Create a leave for employee 2
        lv = LeaveRequest(
            leave_code='LVE-TEST01',
            employee_id=test_data['employee2_id'],
            leave_type='Annual',
            start_date='2026-12-01',
            end_date='2026-12-05',
            reason='Holiday',
            status='Pending'
        )
        db.session.add(lv)
        db.session.commit()
        leave_id = lv.id

    # Employee 1 tries to view employee 2's leave
    emp_token = _login(client, test_data['emp_email'])
    resp = client.get(
        f'/api/leaves/{leave_id}',
        headers={'Authorization': f'Bearer {emp_token}'}
    )
    assert resp.status_code == 403
