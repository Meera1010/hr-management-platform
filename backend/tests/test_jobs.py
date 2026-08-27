import pytest
from app import db
from app.models.department import Department
from app.models.job import Job
from app.models.role import Role

@pytest.fixture
def test_department(app_context):
    dept = Department(name="Engineering Test", description="Test Dept", status="Active")
    db.session.add(dept)
    db.session.commit()
    return dept

def test_create_job_recruiter(client, recruiter_headers, test_department):
    job_data = {
        "job_code": "JOB-001",
        "title": "Software Engineer",
        "department_id": test_department.id,
        "description": "Develop software."
    }
    response = client.post('/api/jobs/', json=job_data, headers=recruiter_headers)
    assert response.status_code == 201
    assert response.json['data']['job_code'] == "JOB-001"

def test_create_job_employee_forbidden(client, employee_headers, test_department):
    job_data = {
        "job_code": "JOB-002",
        "title": "Software Engineer 2",
        "department_id": test_department.id,
        "description": "Develop software."
    }
    response = client.post('/api/jobs/', json=job_data, headers=employee_headers)
    assert response.status_code == 403

def test_get_jobs_employee_sees_open_only(client, recruiter_headers, employee_headers, test_department):
    job1 = Job(job_code="J1", title="Job 1", department_id=test_department.id, description="D", status="Draft")
    job2 = Job(job_code="J2", title="Job 2", department_id=test_department.id, description="D", status="Open")
    db.session.add_all([job1, job2])
    db.session.commit()

    # Employee sees only Open jobs
    response = client.get('/api/jobs/', headers=employee_headers)
    assert response.status_code == 200
    assert len(response.json['data']) == 1
    assert response.json['data'][0]['status'] == 'Open'

    # Recruiter sees both
    response_rec = client.get('/api/jobs/', headers=recruiter_headers)
    assert response_rec.status_code == 200
    assert len(response_rec.json['data']) == 2

def test_archive_job_admin(client, admin_headers, test_department):
    job = Job(job_code="J3", title="Job 3", department_id=test_department.id, description="D", status="Open")
    db.session.add(job)
    db.session.commit()
    
    response = client.delete(f'/api/jobs/{job.id}', headers=admin_headers)
    assert response.status_code == 200
    
    updated_job = Job.query.get(job.id)
    assert updated_job.status == 'Archived'

def test_archive_job_recruiter_forbidden(client, recruiter_headers, test_department):
    job = Job(job_code="J4", title="Job 4", department_id=test_department.id, description="D", status="Open")
    db.session.add(job)
    db.session.commit()
    
    response = client.delete(f'/api/jobs/{job.id}', headers=recruiter_headers)
    assert response.status_code == 403
