"""
Tests for Attendance module — Step 10
Uses fictional demo data. No real personal information.
"""
import pytest
from datetime import date
from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.models.attendance import Attendance


@pytest.fixture
def app():
    from app.config import Config

    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        JWT_SECRET_KEY = 'test-secret-attendance'

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
        # Roles
        emp_role = Role(name='Employee', description='Employee role')
        hr_role = Role(name='HR', description='HR role')
        db.session.add_all([emp_role, hr_role])
        db.session.commit()

        # Department
        dept = Department(name='Engineering', description='Engineering dept', status='Active')
        db.session.add(dept)
        db.session.commit()

        # Employee user
        emp_user = User(first_name='Alex', last_name='Kumar', email='alex@example.com', role_id=emp_role.id)
        emp_user.set_password('testpass123')
        hr_user = User(first_name='HR', last_name='Manager', email='hr@example.com', role_id=hr_role.id)
        hr_user.set_password('testpass123')
        db.session.add_all([emp_user, hr_user])
        db.session.commit()

        # Employee linked to user
        emp = Employee(
            employee_code='TSTEMP001',
            first_name='Alex', last_name='Kumar',
            email='alex.emp@example.com',
            department_id=dept.id,
            user_id=emp_user.id,
            designation='Engineer',
            joining_date=date(2024, 1, 1),
            employment_type='Full Time',
            status='Active'
        )
        db.session.add(emp)
        db.session.commit()

        return {
            'emp_user_id': emp_user.id,
            'hr_user_id': hr_user.id,
            'employee_id': emp.id,
            'emp_email': 'alex@example.com',
            'hr_email': 'hr@example.com',
        }


def _login(client, email, password='testpass123'):
    resp = client.post('/api/auth/login', json={'email': email, 'password': password})
    return resp.get_json()['data']['access_token']


# ─── Test 1: Employee Check-In ────────────────────────────────────────────────

def test_employee_check_in(client, test_data):
    token = _login(client, test_data['emp_email'])
    resp = client.post(
        '/api/attendance/check-in',
        headers={'Authorization': f'Bearer {token}'}
    )
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert 'Check-in successful' in data['message']
    assert data['data']['status'] == 'Present'
    assert data['data']['check_in'] is not None


# ─── Test 2: Duplicate Check-In Prevention ────────────────────────────────────

def test_duplicate_check_in_prevented(client, test_data):
    token = _login(client, test_data['emp_email'])
    # First check-in
    client.post('/api/attendance/check-in', headers={'Authorization': f'Bearer {token}'})
    # Duplicate
    resp = client.post('/api/attendance/check-in', headers={'Authorization': f'Bearer {token}'})
    data = resp.get_json()
    assert resp.status_code == 400
    assert data['success'] is False
    assert 'Already checked in' in data['message']


# ─── Test 3: Employee Check-Out ───────────────────────────────────────────────

def test_employee_check_out(client, test_data):
    token = _login(client, test_data['emp_email'])
    client.post('/api/attendance/check-in', headers={'Authorization': f'Bearer {token}'})
    resp = client.post('/api/attendance/check-out', headers={'Authorization': f'Bearer {token}'})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert 'Check-out successful' in data['message']
    assert data['data']['check_out'] is not None


# ─── Test 4: Duplicate Check-Out Prevention ───────────────────────────────────

def test_duplicate_check_out_prevented(client, test_data):
    token = _login(client, test_data['emp_email'])
    client.post('/api/attendance/check-in', headers={'Authorization': f'Bearer {token}'})
    client.post('/api/attendance/check-out', headers={'Authorization': f'Bearer {token}'})
    resp = client.post('/api/attendance/check-out', headers={'Authorization': f'Bearer {token}'})
    data = resp.get_json()
    assert resp.status_code == 400
    assert data['success'] is False
    assert 'Already checked out' in data['message']


# ─── Test 5: Work Hours Calculation ──────────────────────────────────────────

def test_work_hours_calculation():
    wh = Attendance.calculate_work_hours('09:00:00', '17:30:00')
    assert wh == 8.5

    wh2 = Attendance.calculate_work_hours('09:00:00', '18:00:00')
    assert wh2 == 9.0

    # Checkout before checkin returns None
    wh3 = Attendance.calculate_work_hours('18:00:00', '09:00:00')
    assert wh3 is None


# ─── Test 6: Attendance Summary ───────────────────────────────────────────────

def test_attendance_summary(client, app, test_data):
    with app.app_context():
        # Create test attendance records
        records = [
            Attendance(employee_id=test_data['employee_id'], attendance_date='2026-07-01', status='Present', check_in='09:00:00', check_out='18:00:00', work_hours=9.0),
            Attendance(employee_id=test_data['employee_id'], attendance_date='2026-07-02', status='Absent'),
            Attendance(employee_id=test_data['employee_id'], attendance_date='2026-07-03', status='Work From Home', check_in='09:30:00', check_out='17:30:00', work_hours=8.0),
            Attendance(employee_id=test_data['employee_id'], attendance_date='2026-07-04', status='Half Day'),
        ]
        db.session.add_all(records)
        db.session.commit()
        emp_id = test_data['employee_id']

    token = _login(client, test_data['hr_email'])
    resp = client.get(
        f'/api/attendance/summary/{test_data["employee_id"]}',
        headers={'Authorization': f'Bearer {token}'}
    )
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    summary = data['data']
    assert summary['present_days'] == 1
    assert summary['absent_days'] == 1
    assert summary['wfh_days'] == 1
    assert summary['half_days'] == 1
    assert summary['total_working_days'] == 4
    assert summary['attendance_percentage'] == 25.0


# ─── Test 7: HR Can Create Manual Attendance ──────────────────────────────────

def test_hr_can_create_manual_attendance(client, test_data):
    token = _login(client, test_data['hr_email'])
    resp = client.post(
        '/api/attendance',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'employee_id': test_data['employee_id'],
            'attendance_date': '2026-06-01',
            'status': 'Present',
            'check_in': '09:00:00',
            'check_out': '17:00:00',
            'remarks': 'Manual entry'
        }
    )
    data = resp.get_json()
    assert resp.status_code == 201
    assert data['success'] is True
    assert data['data']['work_hours'] == 8.0


# ─── Test 8: Unauthorized Roles Cannot Check-In ───────────────────────────────

def test_non_employee_cannot_check_in(client, test_data):
    token = _login(client, test_data['hr_email'])
    resp = client.post('/api/attendance/check-in', headers={'Authorization': f'Bearer {token}'})
    data = resp.get_json()
    assert resp.status_code == 403
    assert data['success'] is False
