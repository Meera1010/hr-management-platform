import pytest

def test_asset_category_creation(client, admin_headers):
    res = client.post('/api/assets/categories', json={
        'name': 'MacBook Pro Laptops',
        'code': 'CAT-MACBOOK',
        'description': 'Apple silicon M-series laptops'
    }, headers=admin_headers)

    assert res.status_code == 201
    assert res.json['category']['code'] == 'CAT-MACBOOK'

def test_asset_creation_and_retrieval(client, admin_headers):
    # Create category first
    cat_res = client.post('/api/assets/categories', json={'name': 'Laptops', 'code': 'CAT-LAPTOP'}, headers=admin_headers)
    cat_id = cat_res.json['category']['id']

    res = client.post('/api/assets/', json={
        'asset_tag': 'AST-M3-001',
        'name': 'MacBook Pro 16 M3 Max',
        'category_id': cat_id,
        'serial_number': 'C02GX001M3',
        'purchase_cost': 249900.0,
        'status': 'Available'
    }, headers=admin_headers)

    assert res.status_code == 201
    assert res.json['asset']['asset_tag'] == 'AST-M3-001'

    get_res = client.get('/api/assets/', headers=admin_headers)
    assert get_res.status_code == 200
    assert len(get_res.json['assets']) > 0

def test_asset_assignment_and_return(client, admin_headers):
    cat_res = client.post('/api/assets/categories', json={'name': 'Monitors', 'code': 'CAT-MONITOR'}, headers=admin_headers)
    cat_id = cat_res.json['category']['id']

    ast_res = client.post('/api/assets/', json={
        'asset_tag': 'AST-MON-002',
        'name': 'Dell UltraSharp 27 4K',
        'category_id': cat_id,
        'status': 'Available'
    }, headers=admin_headers)
    asset_id = ast_res.json['asset']['id']

    # Assign
    assign_res = client.post(f'/api/assets/{asset_id}/assign', json={'employee_id': 1}, headers=admin_headers)
    assert assign_res.status_code == 200
    assert assign_res.json['assignment']['status'] == 'Active'

    # Return
    ret_res = client.post(f'/api/assets/{asset_id}/return', json={'condition': 'Excellent'}, headers=admin_headers)
    assert ret_res.status_code == 200
    assert ret_res.json['asset']['status'] == 'Available'

def test_it_ticket_submission(client, hr_headers):
    res = client.post('/api/assets/tickets', json={
        'employee_id': 1,
        'subject': 'Display Flickering Issue',
        'description': 'Secondary monitor flicks when connected via HDMI.',
        'priority': 'Medium'
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['ticket']['status'] == 'Open'
