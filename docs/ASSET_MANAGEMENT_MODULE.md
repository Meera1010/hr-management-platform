# IT Asset & Equipment Lifecycle Management

## Overview
The **Asset & Equipment Sub-System** tracks corporate hardware inventory (laptops, monitors, mobile devices), software licenses, hardware maintenance logs, vendor contracts, IT helpdesk tickets, and asset handover/return workflows during onboarding and exit.

---

## Core Features & Workflows

### 1. Asset Directory & Tagging
- Unique asset tagging (e.g. `AST-MAC-001`), serial number tracking, manufacturer, model name, purchase cost, and warranty expiration dates.
- Status management: `Available`, `Assigned`, `Under Maintenance`, `Retired`, `Lost`.

### 2. Assignment & Handover Lifecycle
- One-click allocation to active employees with digital sign-off.
- Return workflow with condition logging (`New`, `Excellent`, `Good`, `Fair`, `Damaged`).

### 3. IT Helpdesk & Ticketing Integration
- Support ticket creation for hardware faults, software access, network issues.
- Ticket resolution assignment, priority tracking (`Low`, `Medium`, `High`, `Urgent`), and audit resolution notes.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/assets/categories` | List asset categories | All Authenticated |
| `POST` | `/api/assets/categories` | Create asset category | `Admin`, `HR` |
| `GET` | `/api/assets/` | List company assets with filters | All Authenticated |
| `POST` | `/api/assets/` | Register new hardware asset | `Admin`, `HR` |
| `POST` | `/api/assets/<id>/assign` | Assign asset to employee | `Admin`, `HR` |
| `POST` | `/api/assets/<id>/return` | Return asset to stock inventory | `Admin`, `HR` |
| `GET` | `/api/assets/my-assets` | View assets assigned to current user | All Authenticated |
| `GET` | `/api/assets/tickets` | View IT support tickets | All Authenticated |
| `POST` | `/api/assets/tickets` | Create IT support ticket | All Authenticated |
