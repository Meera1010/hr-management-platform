# Employee Lifecycle, Onboarding & Exit Management

## Overview
The **Employee Lifecycle Sub-System** manages pre-onboarding orientation task checklists, buddy/mentor allocation, document verification, resignation requests, notice period calculations, multi-department exit clearances, and Full & Final (FnF) financial settlements.

---

## Onboarding Plan Workflows
- Automated generation of 6-part default onboarding checklist upon new hire creation.
- Role-scoped task assignments (`Employee`, `HR`, `IT Admin`, `Manager`).
- Task completion progress percentage calculation.

## Resignation & Exit Clearance Workflows
- Resignation submission with notice period calculation.
- Departmental clearance workflow across IT, HR, Finance, Admin, and Reporting Managers.
- Full & Final (FnF) settlement computation including unpaid salary, leave encashment, gratuity, and notice period deductions.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/lifecycle/onboarding/checklists` | View onboarding plans | All Authenticated |
| `POST` | `/api/lifecycle/onboarding/checklists/initiate` | Generate onboarding plan for new hire | `Admin`, `HR` |
| `POST` | `/api/lifecycle/onboarding/tasks/<id>/toggle` | Toggle onboarding task status | All Authenticated |
| `GET` | `/api/lifecycle/resignations` | View resignation requests | All Authenticated |
| `POST` | `/api/lifecycle/resignations` | Submit resignation request | All Authenticated |
| `POST` | `/api/lifecycle/resignations/<id>/clearance` | Sign off department clearance | `Admin`, `HR` |
| `GET` | `/api/lifecycle/fnf-settlements` | View FnF settlements | `Admin`, `HR` |
| `POST` | `/api/lifecycle/fnf-settlements/calculate` | Compute FnF net payout | `Admin`, `HR` |
