from app import db
from app.models.assets import Asset, AssetAssignment, AssetMaintenance, SoftwareLicense, ITTicket
from datetime import datetime

class AssetService:
    @staticmethod
    def assign_asset_to_employee(asset_id, employee_id, assigned_by_id, notes=None):
        asset = Asset.query.get_or_404(asset_id)
        if asset.status == 'Assigned':
            raise ValueError(f"Asset {asset.asset_tag} is already assigned.")

        # Deactivate any active assignments
        existing_assignments = AssetAssignment.query.filter_by(asset_id=asset_id, status='Active').all()
        for ea in existing_assignments:
            ea.status = 'Returned'
            ea.returned_date = datetime.utcnow().date()

        assignment = AssetAssignment(
            asset_id=asset_id,
            employee_id=employee_id,
            assigned_date=datetime.utcnow().date(),
            status='Active',
            assigned_by_id=assigned_by_id,
            notes=notes
        )
        asset.status = 'Assigned'
        db.session.add(assignment)
        db.session.commit()
        return assignment

    @staticmethod
    def return_asset(asset_id, condition_on_return='Good', notes=None):
        asset = Asset.query.get_or_404(asset_id)
        assignment = AssetAssignment.query.filter_by(asset_id=asset_id, status='Active').first()
        if assignment:
            assignment.status = 'Returned'
            assignment.returned_date = datetime.utcnow().date()
            assignment.condition_on_return = condition_on_return
            if notes:
                assignment.notes = f"{assignment.notes or ''}\nReturn Note: {notes}"

        asset.status = 'Available'
        asset.condition = condition_on_return
        db.session.commit()
        return asset
