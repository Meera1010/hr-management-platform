import pytest
from app import db
from app.models.department import Department
from app.models.role import Role
from app.models.user import User

@pytest.fixture
def auth_headers(client, app_context):
    # Ensure HR role exists
    role = Role.query.filter_by(name='HR').first()
    if not role:
        role = Role(name='HR', description='HR')
        db.session.add(role)
        db.session.commit()
    
    # Create test user
    user = User(first_name='Test', last_name='HR', email='hr_test@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    res = client.post('/api/auth/login', json={'email': 'hr_test@example.com', 'password': 'password'})
    token = res.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_create_department(client, auth_headers, app_context):
    res = client.post('/api/departments/', headers=auth_headers, json={
        'name': 'Engineering Test',
        'description': 'Tech team'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'Engineering Test'

def test_duplicate_department(client, auth_headers, app_context):
    client.post('/api/departments/', headers=auth_headers, json={'name': 'Duplicate'})
    res = client.post('/api/departments/', headers=auth_headers, json={'name': 'Duplicate'})
    assert res.status_code == 409

def test_get_departments(client, auth_headers, app_context):
    client.post('/api/departments/', headers=auth_headers, json={'name': 'Sales'})
    res = client.get('/api/departments/', headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()['data']) > 0

def test_update_department(client, auth_headers, app_context):
    res = client.post('/api/departments/', headers=auth_headers, json={'name': 'Marketing'})
    dept_id = res.get_json()['data']['id']
    
    res = client.put(f'/api/departments/{dept_id}', headers=auth_headers, json={'status': 'Inactive'})
    assert res.status_code == 200
    assert res.get_json()['data']['status'] == 'Inactive'

def test_delete_department(client, auth_headers, app_context):
    # The route requires admin_required, but the auth_headers fixture creates an HR user.
    # Let's create an Admin user to test delete.
    role = Role.query.filter_by(name='Admin').first()
    if not role:
        role = Role(name='Admin', description='Admin')
        db.session.add(role)
        db.session.commit()
        
    user = User(first_name='Admin', last_name='Admin', email='admin_test2@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    login_res = client.post('/api/auth/login', json={'email': 'admin_test2@example.com', 'password': 'password'})
    token = login_res.get_json()['data']['access_token']
    admin_headers = {'Authorization': f'Bearer {token}'}

    res = client.post('/api/departments/', headers=admin_headers, json={'name': 'To Delete'})
    dept_id = res.get_json()['data']['id']
    
    res = client.delete(f'/api/departments/{dept_id}', headers=admin_headers)
    assert res.status_code == 200
    assert res.get_json()['data']['status'] == 'Inactive'
