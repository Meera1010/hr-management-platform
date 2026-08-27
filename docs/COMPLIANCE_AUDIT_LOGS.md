# Grievance Handling, HR Policies & Audit Trails

## Overview
The **Compliance & Audit Sub-System** handles confidential grievance reporting (with anonymous reporting options), investigation ticket escalation, central policy document publishing with mandatory employee digital acknowledgment, and a full system audit trail tracking sensitive entity mutations.

---

## Core Features
- Confidential grievance tickets with severity ratings (`Low`, `Medium`, `High`, `Critical`).
- Company policy library with versioning (`v1.0`, `v2.0`) and IP-stamped digital acknowledgment records.
- Immutable audit log recorder capturing user ID, IP address, timestamp, action type (`CREATE`, `UPDATE`, `DELETE`), entity type, and delta details.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/compliance/grievances` | View grievance tickets | All Authenticated |
| `POST` | `/api/compliance/grievances` | Submit grievance ticket | All Authenticated |
| `GET` | `/api/compliance/policies` | View published policy documents | All Authenticated |
| `POST` | `/api/compliance/policies/<id>/acknowledge` | Acknowledge company policy | All Authenticated |
| `GET` | `/api/compliance/audit-logs` | View audit trail records | `Admin`, `HR` |
