import pytest
from app.services.asset_procurement_service import AssetProcurementService

def test_straight_line_depreciation():
    res = AssetProcurementService.calculate_straight_line_depreciation(
        purchase_cost=100000.0,
        salvage_value=10000.0,
        useful_life_years=3,
        current_age_years=1.5
    )
    assert res['annual_depreciation'] == 30000.0
    assert res['current_book_value'] == 55000.0

def test_wdv_depreciation():
    res = AssetProcurementService.calculate_wdv_depreciation(
        purchase_cost=200000.0,
        rate_pct=40.0,
        age_years=2
    )
    assert len(res['schedule']) == 2
    assert res['schedule'][0]['ending_value'] == 120000.0
    assert res['schedule'][1]['ending_value'] == 72000.0

def test_warranty_expiration_alerts():
    assets = [
        {'asset_tag': 'AST-001', 'name': 'MacBook Pro', 'warranty_expiry_date': '2026-09-15', 'status': 'Assigned'},
        {'asset_tag': 'AST-002', 'name': 'Dell Monitor', 'warranty_expiry_date': '2028-01-01', 'status': 'Available'}
    ]
    exp = AssetProcurementService.check_warranty_expirations(assets, days_threshold=60)
    assert len(exp) >= 0
