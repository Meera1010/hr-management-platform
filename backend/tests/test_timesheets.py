import pytest

def test_timesheet_submission(client, hr_headers):
    res = client.post('/api/timesheets/weekly', json={
        'employee_id': 1,
        'week_start_date': '2026-05-04',
        'week_end_date': '2026-05-10',
        'entries': [
            {'entry_date': '2026-05-04', 'project_name': 'AI HR Platform', 'task_description': 'Backend API development', 'hours_logged': 8.0, 'is_billable': True},
            {'entry_date': '2026-05-05', 'project_name': 'AI HR Platform', 'task_description': 'Database schema design', 'hours_logged': 8.0, 'is_billable': True}
        ]
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['timesheet']['total_hours'] == 16.0
    assert res.json['timesheet']['billable_hours'] == 16.0

def test_shift_rosters_retrieval(client, hr_headers):
    res = client.get('/api/timesheets/rosters', headers=hr_headers)
    assert res.status_code == 200
