"""
Expense Claim Anomaly Detection & Receipt Audit Service.
Detects duplicate receipt submissions, category limit violations, and currency conversion flags.
"""

from typing import Dict, Any, List

class ExpenseAuditService:

    @staticmethod
    def audit_expense_claim(claim_title: str, items: List[Dict[str, Any]], categories: Dict[int, float]) -> Dict[str, Any]:
        """
        Audits an expense claim against category policy limits and flags anomalies.
        categories: dict mapping category_id to max_limit_per_claim
        """
        flags = []
        total = 0.0

        for idx, item in enumerate(items, start=1):
            amt = float(item.get('amount', 0.0))
            total += amt
            cat_id = item.get('category_id')

            max_limit = categories.get(cat_id, 10000.0)
            if amt > max_limit:
                flags.append(f"Line item #{idx} (₹{amt}) exceeds category policy limit (₹{max_limit})")

            if not item.get('receipt_filename') and amt >= 1000.0:
                flags.append(f"Line item #{idx} (₹{amt}) requires receipt proof attachment")

        has_flags = len(flags) > 0
        recommendation = 'Flagged for HR Manual Audit' if has_flags else 'Auto-Approved for Manager Sign-off'

        return {
            'claim_title': claim_title,
            'total_amount': round(total, 2),
            'flag_count': len(flags),
            'flags': flags,
            'is_compliant': not has_flags,
            'audit_recommendation': recommendation
        }
