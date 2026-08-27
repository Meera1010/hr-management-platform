from datetime import datetime
import pytest
from app import db
from app.models.training import TrainingCourse, TrainingAssignment
from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User

def test_create_and_get_courses(client, admin_headers):
    # Create course
    res = client.post('/api/training/courses', json={
        'title': 'Cybersecurity Fundamentals',
        'category': 'Compliance',
        'description': 'Basic security hygiene.',
        'duration_hours': 3,
        'instructor': 'Security Team'
    }, headers=admin_headers)

    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'Cybersecurity Fundamentals'

    # Get courses list
    get_res = client.get('/api/training/courses', headers=admin_headers)
    assert get_res.status_code == 200
    c_data = get_res.get_json()
    assert c_data['count'] >= 1

def test_assign_and_complete_training(client, admin_headers, employee_headers, app_context):
    with app_context.app_context():
        # Ensure department & employee exist for test
        dept = Department(name='Test Engineering', description='Eng dept')
        db.session.add(dept)
        db.session.commit()

        emp_user = User.query.filter_by(email='employee_test@example.com').first()
        emp = Employee(
            employee_code='EMP-TRN-TEST',
            first_name='Test',
            last_name='Emp',
            email='employee_test@example.com',
            department_id=dept.id,
            user_id=emp_user.id if emp_user else None,
            designation='Software Engineer',
            joining_date=datetime.now().date(),
            employment_type='Full-Time',
            status='Active'
        )
        db.session.add(emp)

        course = TrainingCourse(
            course_code='TRN-TEST-1',
            title='Test Course',
            category='Technical',
            duration_hours=2
        )
        db.session.add(course)
        db.session.commit()

        emp_id = emp.id
        course_id = course.id

    # Assign training
    assign_res = client.post('/api/training/assignments', json={
        'course_id': course_id,
        'employee_id': emp_id,
        'due_date': '2026-10-30'
    }, headers=admin_headers)

    assert assign_res.status_code == 201
    assign_data = assign_res.get_json()
    assert assign_data['success'] is True
    assignment_id = assign_data['data']['id']

    # Employee get my trainings
    my_res = client.get('/api/training/my-trainings', headers=employee_headers)
    assert my_res.status_code == 200

    # Complete assignment
    up_res = client.put(f'/api/training/assignments/{assignment_id}', json={
        'status': 'Completed',
        'feedback': 'Great learning experience!',
        'score': 98.0
    }, headers=employee_headers)

    assert up_res.status_code == 200
    assert up_res.get_json()['data']['status'] == 'Completed'
