def test_health_endpoint_returns_success(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert data['message'] == 'AI HR Platform API is running'
    assert data['database'] == 'connected'


def test_root_landing_responds(client):
    res = client.get('/')
    assert res.status_code == 200
    assert 'AI HR Platform' in res.get_data(as_text=True)
