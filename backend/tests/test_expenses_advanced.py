import pytest
from app.services.expense_audit_service import ExpenseAuditService

def test_expense_audit_service_compliant():
    categories = {1: 5000.0, 2: 10000.0}
    items = [
        {'category_id': 1, 'amount': 1500.0, 'receipt_filename': 'receipt1.png'},
        {'category_id': 2, 'amount': 3000.0, 'receipt_filename': 'receipt2.png'}
    ]
    res = ExpenseAuditService.audit_expense_claim('Client Dinner', items, categories)
    assert res['is_compliant'] is True
    assert res['total_amount'] == 4500.0
    assert len(res['flags']) == 0

def test_expense_audit_service_flagged():
    categories = {1: 1000.0}
    items = [
        {'category_id': 1, 'amount': 2500.0, 'receipt_filename': None}
    ]
    res = ExpenseAuditService.audit_expense_claim('Over Limit Taxi', items, categories)
    assert res['is_compliant'] is False
    assert len(res['flags']) >= 1
