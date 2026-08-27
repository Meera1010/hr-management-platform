import pytest
from app.services.compliance_audit_engine import ComplianceAuditEngine

def test_grievance_sla_target():
    assert ComplianceAuditEngine.calculate_grievance_sla_target('Critical') == 2
    assert ComplianceAuditEngine.calculate_grievance_sla_target('High') == 5
    assert ComplianceAuditEngine.calculate_grievance_sla_target('Medium') == 10
    assert ComplianceAuditEngine.calculate_grievance_sla_target('Low') == 15

def test_entity_diff_generation():
    old = {'status': 'Pending', 'salary': 50000.0}
    new = {'status': 'Approved', 'salary': 50000.0}

    diff_str = ComplianceAuditEngine.generate_entity_diff(old, new)
    assert 'status' in diff_str
    assert 'Approved' in diff_str
