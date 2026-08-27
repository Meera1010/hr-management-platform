import pytest
from datetime import date, timedelta
from app.utils.asset_depreciation_engine import AssetDepreciationEngine
from app.services.asset_procurement_service import AssetProcurementService

def test_straight_line_depreciation():
    result = AssetDepreciationEngine.calculate_straight_line_depreciation(100000.0, 10000.0, 5)
    assert result['annual_depreciation'] == 18000.0
    assert result['monthly_depreciation'] == 1500.0

def test_written_down_value_depreciation():
    result = AssetDepreciationEngine.calculate_wdv_depreciation(100000.0, 40.0, 3)
    assert len(result['schedule']) == 3
    assert result['schedule'][0]['depreciation_amount'] == 40000.0
    assert result['schedule'][0]['closing_book_value'] == 60000.0

def test_vendor_warranty_evaluation():
    expiring_date = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')
    future_date = (date.today() + timedelta(days=120)).strftime('%Y-%m-%d')

    expiring = AssetProcurementService.check_warranty_expirations([
        {'asset_tag': 'AST-01', 'name': 'MacBook Pro', 'warranty_expiry_date': expiring_date},
        {'asset_tag': 'AST-02', 'name': 'Dell Monitor', 'warranty_expiry_date': future_date}
    ])
    assert len(expiring) == 1
    assert expiring[0]['asset_tag'] == 'AST-01'
