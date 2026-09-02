import os
import sys
import pytest
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app import create_app, db
from app.config import Config
from app.models.user import User
from app.models.role import Role
from flask_jwt_extended import create_access_token

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': StaticPool,
        'connect_args': {'check_same_thread': False}
    }
    JWT_SECRET_KEY = 'test-jwt-secret-very-secure-32-chars-long-key!'

@pytest.fixture
def client():
    app = create_app(TestConfig)
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Seed basic roles safely
            role = Role.query.filter_by(name='Admin').first()
            if not role:
                role = Role(name='Admin', description='Admin role')
                db.session.add(role)
                db.session.commit()
                
            admin = User(first_name='Sys', last_name='Admin', email='admin@test.com', role_id=role.id)
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            
        yield client

@pytest.fixture
def auth_headers(client):
    with client.application.app_context():
        admin = User.query.filter_by(email='admin@test.com').first()
        token = create_access_token(identity=str(admin.id))
        return {'Authorization': f'Bearer {token}'}

def test_database_connection(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_role_creation(client):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        assert role is not None

def test_user_creation(client, auth_headers):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        role_id = role.id

    response = client.post('/api/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password': 'password123',
        'role_id': role_id
    }, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json['success'] is True

def test_duplicate_email(client, auth_headers):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        role_id = role.id
        
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test2@example.com',
        'password': 'password123',
        'role_id': role_id
    }
    client.post('/api/users/', json=data, headers=auth_headers)
    response = client.post('/api/users/', json=data, headers=auth_headers)
    
    assert response.status_code == 400
    assert response.json['success'] is False
    assert "Email already exists" in response.json['message']

def test_invalid_email(client, auth_headers):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        role_id = role.id
        
    response = client.post('/api/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'invalid-email',
        'password': 'password123',
        'role_id': role_id
    }, headers=auth_headers)
    
    assert response.status_code == 400
    assert "Valid email is required" in response.json['message']

def test_password_hashing(client):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        user = User(first_name="A", last_name="B", email="a@b.com", role_id=role.id)
        user.set_password("mypassword")
        assert user.password_hash != "mypassword"
        assert user.check_password("mypassword") is True
        assert user.check_password("wrong") is False

def test_user_update(client, auth_headers):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        role_id = role.id
        
    post_res = client.post('/api/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'update@example.com',
        'password': 'password123',
        'role_id': role_id
    }, headers=auth_headers)
    
    user_id = post_res.json['data']['id']
    
    response = client.put(f'/api/users/{user_id}', json={
        'first_name': 'UpdatedName'
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['data']['first_name'] == 'UpdatedName'

def test_user_deactivation(client, auth_headers):
    with client.application.app_context():
        role = Role.query.filter_by(name='Admin').first()
        role_id = role.id
        
    post_res = client.post('/api/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'deact@example.com',
        'password': 'password123',
        'role_id': role_id
    }, headers=auth_headers)
    
    user_id = post_res.json['data']['id']
    
    response = client.delete(f'/api/users/{user_id}', headers=auth_headers)
    assert response.status_code == 200
    
    get_res = client.get(f'/api/users/{user_id}', headers=auth_headers)
    assert get_res.json['data']['is_active'] is False

def test_role_retrieval(client, auth_headers):
    response = client.get('/api/roles/', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['data']) >= 1
