"""
Audit Trail Serializer & Compliance Activity Delta Recorder.
Provides structured JSON serialization of sensitive HR record changes, RBAC role updates,
and salary adjustment logs.
"""

import json
from typing import Dict, Any
from datetime import datetime, date

def default_json_serializer(obj: Any) -> Any:
    """JSON serializer helper for datetime and date objects."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def serialize_audit_event(user_id: int, user_email: str, action: str, target_entity: str, entity_id: int, changes: Dict[str, Any]) -> Dict[str, Any]:
    """Generates structured audit log record entry."""
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'user_email': user_email,
        'action': action.upper(),
        'target_entity': target_entity,
        'entity_id': entity_id,
        'changes_json': json.dumps(changes, default=default_json_serializer)
    }
