"""
Grievance Case Escalation & Audit Trail Diff Recorder.
Tracks confidential HR compliance cases, POSH investigation milestones,
and serializes entity state mutations for audit logging.
"""

import json
from typing import Dict, Any

class ComplianceAuditEngine:

    @staticmethod
    def calculate_grievance_sla_target(severity: str) -> int:
        """Returns SLA resolution target days based on grievance severity."""
        sev = (severity or '').capitalize()
        if sev == 'Critical':
            return 2   # 48 hours
        elif sev == 'High':
            return 5   # 5 business days
        elif sev == 'Medium':
            return 10  # 10 business days
        else:
            return 15  # 15 business days

    @staticmethod
    def generate_entity_diff(old_dict: Dict[str, Any], new_dict: Dict[str, Any]) -> str:
        """Computes JSON delta of modified fields for security audit trail recording."""
        changes = {}
        all_keys = set(old_dict.keys()).union(set(new_dict.keys()))

        for k in all_keys:
            old_val = old_dict.get(k)
            new_val = new_dict.get(k)
            if old_val != new_val:
                changes[k] = {'old': old_val, 'new': new_val}

        return json.dumps(changes, default=str)
