import pytest
from app.models.notification import Notification
from app.models.user import User

def test_notification_flow(client, employee_headers, app_context):
    with app_context.app_context():
        emp_user = User.query.filter_by(email='employee_test@example.com').first()
        if not emp_user:
            emp_user = User.query.first()
        user_id = emp_user.id

        # Create test notification
        Notification.create_notification(
            user_id=user_id,
            title='Test Alert',
            message='Unit test notification message',
            type='info'
        )

    # Get notifications
    res = client.get('/api/notifications', headers=employee_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert len(data['data']) >= 1

    notif_id = data['data'][0]['id']

    # Mark single read
    read_res = client.put(f'/api/notifications/{notif_id}/read', headers=employee_headers)
    assert read_res.status_code == 200
    assert read_res.get_json()['data']['is_read'] is True

    # Mark all read
    all_res = client.put('/api/notifications/read-all', headers=employee_headers)
    assert all_res.status_code == 200

    # Delete notification
    del_res = client.delete(f'/api/notifications/{notif_id}', headers=employee_headers)
    assert del_res.status_code == 200
