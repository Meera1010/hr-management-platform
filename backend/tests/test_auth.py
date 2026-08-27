import pytest
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    JWT_SECRET_KEY = 'test-jwt-secret'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Create roles
        roles = ['Admin', 'HR', 'Recruiter', 'Employee', 'Candidate', 'Interviewer']
        for r in roles:
            db.session.add(Role(name=r))
        db.session.commit()
        
        # Create an active admin user
        admin_role = Role.query.filter_by(name='Admin').first()
        admin = User(first_name='Sys', last_name='Admin', email='admin@test.com', role_id=admin_role.id)
        admin.set_password('Admin@123')
        db.session.add(admin)
        
        # Create an inactive user
        hr_role = Role.query.filter_by(name='HR').first()
        inactive = User(first_name='In', last_name='Active', email='inactive@test.com', role_id=hr_role.id, is_active=False)
        inactive.set_password('HR@123')
        db.session.add(inactive)
        
        db.session.commit()
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_valid_login(client):
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'Admin@123'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert 'access_token' in data['data']
    assert 'password' not in data['data']['user']
    assert 'password_hash' not in data['data']['user']

def test_invalid_login(client):
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'WrongPassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['success'] is False
    assert data['message'] == 'Invalid credentials'

def test_inactive_user_login(client):
    response = client.post('/api/auth/login', json={
        'email': 'inactive@test.com',
        'password': 'HR@123'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['success'] is False
    assert data['message'] == 'Authentication required'

def test_missing_credentials(client):
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['success'] is False
    assert data['message'] == 'Email and password are required'

def test_me_endpoint(client):
    # First login to get token
    login_res = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'Admin@123'
    })
    token = login_res.get_json()['data']['access_token']
    
    # Use token to get me
    response = client.get('/api/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['data']['email'] == 'admin@test.com'
    assert 'password' not in data['data']

def test_change_password(client):
    # First login to get token
    login_res = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'Admin@123'
    })
    token = login_res.get_json()['data']['access_token']
    
    # Change password
    change_res = client.post('/api/auth/change-password', json={
        'current_password': 'Admin@123',
        'new_password': 'NewPassword@123'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert change_res.status_code == 200
    
    # Login with new password
    login_new = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'NewPassword@123'
    })
    assert login_new.status_code == 200

def test_unauthorized_access(client):
    # Try to access a protected route without token
    response = client.get('/api/users/')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Authentication required'
