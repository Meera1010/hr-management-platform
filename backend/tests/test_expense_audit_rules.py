import pytest
from app.services.expense_audit_service import ExpenseAuditService

def test_expense_policy_limit_audit_pass():
    audit = ExpenseAuditService.audit_expense_claim(
        claim_title='Onsite Client Visit',
        items=[{'category_id': 1, 'amount': 1200.0, 'receipt_filename': 'receipt.pdf'}],
        categories={1: 1500.0}
    )
    assert audit['is_compliant'] is True
    assert audit['flag_count'] == 0

def test_expense_policy_limit_audit_exceeded():
    audit = ExpenseAuditService.audit_expense_claim(
        claim_title='Onsite Client Visit',
        items=[{'category_id': 1, 'amount': 2500.0, 'receipt_filename': 'receipt.pdf'}],
        categories={1: 1500.0}
    )
    assert audit['is_compliant'] is False
    assert audit['flag_count'] == 1
    assert 'exceeds category policy limit' in audit['flags'][0]

def test_expense_missing_receipt_proof():
    audit = ExpenseAuditService.audit_expense_claim(
        claim_title='Dinner',
        items=[{'category_id': 2, 'amount': 1500.0, 'receipt_filename': None}],
        categories={2: 5000.0}
    )
    assert audit['is_compliant'] is False
    assert 'requires receipt proof attachment' in audit['flags'][0]
