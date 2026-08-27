import pytest
from app import create_app, db
from app.config import Config
from app.models.user import User
from app.models.role import Role
from flask_jwt_extended import create_access_token

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-jwt-secret'

@pytest.fixture
def app_context():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app_context):
    with app_context.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client, app_context):
    role = Role.query.filter_by(name='Admin').first()
    if not role:
        role = Role(name='Admin', description='Admin')
        db.session.add(role)
        db.session.commit()
    user = User(first_name='Admin', last_name='Test', email='admin@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(client, app_context):
    role = Role.query.filter_by(name='Admin').first()
    if not role:
        role = Role(name='Admin', description='Admin')
        db.session.add(role)
        db.session.commit()
    user = User.query.filter_by(email='admin_emp_test@example.com').first()
    if not user:
        user = User(first_name='Admin', last_name='Test', email='admin_emp_test@example.com', role_id=role.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def recruiter_headers(client, app_context):
    role = Role.query.filter_by(name='Recruiter').first()
    if not role:
        role = Role(name='Recruiter', description='Recruiter')
        db.session.add(role)
        db.session.commit()
    user = User(first_name='Recruiter', last_name='Test', email='recruiter_test@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def employee_headers(client, app_context):
    role = Role.query.filter_by(name='Employee').first()
    if not role:
        role = Role(name='Employee', description='Employee')
        db.session.add(role)
        db.session.commit()
    user = User(first_name='Employee', last_name='Test', email='employee_test@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {token}'}
