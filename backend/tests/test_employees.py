import pytest
from app import db
from app.models.employee import Employee
from app.models.department import Department
from app.models.role import Role
from app.models.user import User

@pytest.fixture
def test_department(app_context):
    dept = Department(name='Test Dept', description='Test')
    db.session.add(dept)
    db.session.commit()
    return dept



def test_create_employee(client, admin_headers, test_department, app_context):
    res = client.post('/api/employees/', headers=admin_headers, json={
        'employee_code': 'EMP001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'department_id': test_department.id,
        'designation': 'Software Engineer',
        'joining_date': '2023-01-15',
        'employment_type': 'Full Time'
    })
    
    assert res.status_code == 201
    data = res.get_json()['data']
    assert data['employee_code'] == 'EMP001'
    assert data['first_name'] == 'John'

def test_duplicate_employee_code(client, admin_headers, test_department, app_context):
    payload = {
        'employee_code': 'EMP002',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'department_id': test_department.id,
        'designation': 'Manager',
        'joining_date': '2023-02-01',
        'employment_type': 'Full Time'
    }
    client.post('/api/employees/', headers=admin_headers, json=payload)
    
    # Try again with same code
    payload['email'] = 'jane.doe2@example.com' # Change email to ensure it fails on code
    res = client.post('/api/employees/', headers=admin_headers, json=payload)
    assert res.status_code == 409

def test_search_employees(client, admin_headers, test_department, app_context):
    client.post('/api/employees/', headers=admin_headers, json={
        'employee_code': 'EMP003',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'department_id': test_department.id,
        'designation': 'Designer',
        'joining_date': '2023-03-01',
        'employment_type': 'Full Time'
    })
    
    res = client.get('/api/employees/search?q=Alice', headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()['data']
    assert len(data) > 0
    assert data[0]['first_name'] == 'Alice'

def test_employee_rbac(client, test_department, app_context):
    # Create Candidate User
    role = Role.query.filter_by(name='Candidate').first()
    if not role:
        role = Role(name='Candidate', description='Candidate')
        db.session.add(role)
        db.session.commit()
        
    user = User(first_name='Cand', last_name='Test', email='cand_test@example.com', role_id=role.id)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    res = client.post('/api/auth/login', json={'email': 'cand_test@example.com', 'password': 'password'})
    token = res.get_json()['data']['access_token']
    cand_headers = {'Authorization': f'Bearer {token}'}
    
    # Verify Candidate cannot get employees
    res = client.get('/api/employees/', headers=cand_headers)
    assert res.status_code == 403
