# Timesheets, Shift Scheduling & Roster Management

## Overview
The **Timesheet & Shift Sub-System** handles weekly/monthly project time logging, billable vs non-billable hours tracking, shift roster planning (Morning, General, Night, Rotating shifts), and overtime (OT) claim submission and approval workflows.

---

## Core Workflows
- Weekly timesheet logging per project and task.
- Automated billable hours summary calculation.
- Shift roster scheduling per employee per day.
- Overtime claim logging with hourly rate computation.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/timesheets/weekly` | View weekly timesheets | All Authenticated |
| `POST` | `/api/timesheets/weekly` | Submit weekly timesheet | All Authenticated |
| `GET` | `/api/timesheets/shifts` | List active shift definitions | All Authenticated |
| `GET` | `/api/timesheets/rosters` | View shift roster schedule | All Authenticated |
| `GET` | `/api/timesheets/overtime-claims` | View overtime claims | All Authenticated |
