from datetime import datetime
from app import db

class ExpenseCategory(db.Model):
    __tablename__ = 'expense_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    max_limit_per_claim = db.Column(db.Float, default=10000.0)
    requires_receipt = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'max_limit_per_claim': self.max_limit_per_claim,
            'requires_receipt': self.requires_receipt,
            'is_active': self.is_active
        }


class ExpenseClaim(db.Model):
    __tablename__ = 'expense_claims'

    id = db.Column(db.Integer, primary_key=True)
    claim_number = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    claim_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(30), default='Submitted')  # Draft, Submitted, Manager Approved, Finance Approved, Rejected, Paid
    manager_approver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    finance_approver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    payment_reference = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='expense_claims', lazy=True)
    items = db.relationship('ExpenseItem', backref='claim', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'claim_number': self.claim_number,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'title': self.title,
            'claim_date': self.claim_date.strftime('%Y-%m-%d') if self.claim_date else None,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'status': self.status,
            'rejection_reason': self.rejection_reason,
            'payment_reference': self.payment_reference,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class ExpenseItem(db.Model):
    __tablename__ = 'expense_items'

    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('expense_claims.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'), nullable=False)
    item_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    receipt_filename = db.Column(db.String(255), nullable=True)

    category = db.relationship('ExpenseCategory', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'claim_id': self.claim_id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'item_date': self.item_date.strftime('%Y-%m-%d') if self.item_date else None,
            'description': self.description,
            'amount': self.amount,
            'receipt_filename': self.receipt_filename
        }


class TravelRequest(db.Model):
    __tablename__ = 'travel_requests'

    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    estimated_cost = db.Column(db.Float, default=0.0)
    advance_amount_requested = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Submitted')  # Submitted, Approved, Rejected, Completed
    approver_comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='travel_requests', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'request_number': self.request_number,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'destination': self.destination,
            'purpose': self.purpose,
            'departure_date': self.departure_date.strftime('%Y-%m-%d') if self.departure_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'estimated_cost': self.estimated_cost,
            'advance_amount_requested': self.advance_amount_requested,
            'status': self.status,
            'approver_comments': self.approver_comments,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
