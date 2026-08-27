from app import db
from app.models.compliance_audit import AuditLog, GrievanceTicket, GrievanceLog
from datetime import datetime

class ComplianceService:
    @staticmethod
    def log_audit(action, entity_type, entity_id=None, user_id=None, user_email=None, details=None, ip_address=None):
        try:
            log = AuditLog(
                user_id=user_id,
                user_email=user_email,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                details=details,
                ip_address=ip_address,
                timestamp=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()
            return log
        except Exception:
            db.session.rollback()
            return None
