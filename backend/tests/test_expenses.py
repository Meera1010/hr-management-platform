import pytest

def test_expense_claim_submission(client, hr_headers):
    # Get categories first
    c_res = client.get('/api/expenses/categories', headers=hr_headers)

    res = client.post('/api/expenses/claims', json={
        'employee_id': 1,
        'title': 'Client Onsite Travel & Lunch',
        'currency': 'INR',
        'items': [
            {'category_id': 1, 'item_date': '2026-05-01', 'description': 'Taxi cab fare to airport', 'amount': 1500.0},
            {'category_id': 1, 'item_date': '2026-05-01', 'description': 'Client dinner sync', 'amount': 2500.0}
        ]
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['claim']['total_amount'] == 4000.0

def test_travel_request_submission(client, hr_headers):
    res = client.post('/api/expenses/travel-requests', json={
        'employee_id': 1,
        'destination': 'Bengaluru, India',
        'purpose': 'Annual Tech Leadership Summit',
        'departure_date': '2026-06-10',
        'return_date': '2026-06-12',
        'estimated_cost': 25000.0
    }, headers=hr_headers)

    assert res.status_code == 201
    assert res.json['travel_request']['destination'] == 'Bengaluru, India'
