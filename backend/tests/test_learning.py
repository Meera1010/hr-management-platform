import pytest

def test_course_creation_and_enrollment(client, hr_headers):
    c_res = client.post('/api/learning/courses', json={
        'title': 'Advanced Cybersecurity Standards',
        'code': 'SEC-401',
        'category': 'Security',
        'duration_hours': 10.0,
        'is_mandatory': True
    }, headers=hr_headers)

    assert c_res.status_code == 201
    course_id = c_res.json['course']['id']

    # Enroll
    e_res = client.post('/api/learning/enrollments', json={
        'course_id': course_id,
        'employee_id': 1
    }, headers=hr_headers)

    assert e_res.status_code in [200, 201]

def test_certificates_retrieval(client, hr_headers):
    res = client.get('/api/learning/certificates', headers=hr_headers)
    assert res.status_code == 200
