from datetime import datetime
from app import db

class AssetCategory(db.Model):
    __tablename__ = 'asset_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assets = db.relationship('Asset', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('asset_categories.id'), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=True)
    model_name = db.Column(db.String(100), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.Date, nullable=True)
    purchase_cost = db.Column(db.Float, default=0.0)
    warranty_expiry_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Available')  # Available, Assigned, Under Maintenance, Retired, Lost
    condition = db.Column(db.String(30), default='Excellent')  # New, Excellent, Good, Fair, Damaged
    location = db.Column(db.String(100), default='Headquarters')
    vendor_name = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('AssetAssignment', backref='asset', lazy=True)
    maintenance_logs = db.relationship('AssetMaintenance', backref='asset', lazy=True)

    def to_dict(self):
        active_assignment = next((a for a in self.assignments if a.status == 'Active'), None)
        return {
            'id': self.id,
            'asset_tag': self.asset_tag,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'serial_number': self.serial_number,
            'model_name': self.model_name,
            'manufacturer': self.manufacturer,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d') if self.purchase_date else None,
            'purchase_cost': self.purchase_cost,
            'warranty_expiry_date': self.warranty_expiry_date.strftime('%Y-%m-%d') if self.warranty_expiry_date else None,
            'status': self.status,
            'condition': self.condition,
            'location': self.location,
            'vendor_name': self.vendor_name,
            'notes': self.notes,
            'assigned_to_employee': f"{active_assignment.employee.first_name} {active_assignment.employee.last_name}" if active_assignment and active_assignment.employee else None,
            'assigned_employee_id': active_assignment.employee_id if active_assignment else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AssetAssignment(db.Model):
    __tablename__ = 'asset_assignments'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    assigned_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    returned_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Active')  # Active, Returned, Damaged
    condition_on_assignment = db.Column(db.String(30), default='Good')
    condition_on_return = db.Column(db.String(30), nullable=True)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='asset_assignments', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'asset_tag': self.asset.asset_tag if self.asset else None,
            'asset_name': self.asset.name if self.asset else None,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'assigned_date': self.assigned_date.strftime('%Y-%m-%d') if self.assigned_date else None,
            'returned_date': self.returned_date.strftime('%Y-%m-%d') if self.returned_date else None,
            'status': self.status,
            'condition_on_assignment': self.condition_on_assignment,
            'condition_on_return': self.condition_on_return,
            'notes': self.notes
        }


class AssetMaintenance(db.Model):
    __tablename__ = 'asset_maintenances'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    maintenance_type = db.Column(db.String(50), default='Repair')  # Repair, Calibration, Routine, Upgrade
    issue_description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, default=0.0)
    service_provider = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='In Progress')  # Scheduled, In Progress, Completed, Cancelled
    resolution_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'asset_name': self.asset.name if self.asset else None,
            'asset_tag': self.asset.asset_tag if self.asset else None,
            'maintenance_type': self.maintenance_type,
            'issue_description': self.issue_description,
            'cost': self.cost,
            'service_provider': self.service_provider,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'completion_date': self.completion_date.strftime('%Y-%m-%d') if self.completion_date else None,
            'status': self.status,
            'resolution_notes': self.resolution_notes
        }


class SoftwareLicense(db.Model):
    __tablename__ = 'software_licenses'

    id = db.Column(db.Integer, primary_key=True)
    software_name = db.Column(db.String(150), nullable=False)
    license_key = db.Column(db.String(150), nullable=True)
    vendor = db.Column(db.String(100), nullable=True)
    total_seats = db.Column(db.Integer, default=1)
    assigned_seats = db.Column(db.Integer, default=0)
    cost_per_seat = db.Column(db.Float, default=0.0)
    purchase_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'software_name': self.software_name,
            'license_key': self.license_key,
            'vendor': self.vendor,
            'total_seats': self.total_seats,
            'assigned_seats': self.assigned_seats,
            'available_seats': self.total_seats - self.assigned_seats,
            'cost_per_seat': self.cost_per_seat,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'is_active': self.is_active
        }


class ITTicket(db.Model):
    __tablename__ = 'it_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)
    category = db.Column(db.String(50), default='Hardware')  # Hardware, Software, Network, Access Request, Other
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Urgent
    status = db.Column(db.String(30), default='Open')  # Open, In Progress, Resolved, Closed
    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolution_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    employee = db.relationship('Employee', backref='it_tickets', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'asset_id': self.asset_id,
            'category': self.category,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }
