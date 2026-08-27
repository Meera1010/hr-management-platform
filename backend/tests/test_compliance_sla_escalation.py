import pytest
import json
from app.services.compliance_audit_engine import ComplianceAuditEngine

def test_grievance_sla_target_evaluation():
    target = ComplianceAuditEngine.calculate_grievance_sla_target('Critical')
    assert target == 2

def test_grievance_sla_medium():
    target = ComplianceAuditEngine.calculate_grievance_sla_target('Medium')
    assert target == 10

def test_audit_log_diff_serialization():
    diff_str = ComplianceAuditEngine.generate_entity_diff(
        old_dict={'status': 'Active', 'salary': 50000},
        new_dict={'status': 'Active', 'salary': 60000}
    )
    diff = json.loads(diff_str)
    assert 'salary' in diff
    assert diff['salary']['old'] == 50000
    assert diff['salary']['new'] == 60000
