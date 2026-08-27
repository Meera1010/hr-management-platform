from app import db
from app.models.expense_travel import ExpenseClaim, ExpenseItem, ExpenseCategory
import uuid
from datetime import datetime

class ExpenseService:
    @staticmethod
    def recalculate_claim_total(claim_id):
        claim = ExpenseClaim.query.get_or_404(claim_id)
        total = sum(item.amount for item in claim.items)
        claim.total_amount = round(total, 2)
        db.session.commit()
        return claim
