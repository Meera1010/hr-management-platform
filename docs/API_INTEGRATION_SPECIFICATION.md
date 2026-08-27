# REST API Integration Specification & Payload Schemas

## Overview
This document specifies the complete REST API interface contract, payload schemas, error formats, and HTTP status code definitions for all 13 sub-systems in the **AI-Powered HR Platform**.

---

## Global API Standards

### Base URL & Routing
- Production Endpoint: `https://api.hrplatform.internal/api/v1`
- Development Local: `http://localhost:5000/api`

### Standard Headers
```http
Content-Type: application/json
Authorization: Bearer <jwt_access_token>
```

### Response Envelope Format
All API endpoints return JSON payloads following this standardized structure:
```json
{
  "success": true,
  "message": "Resource retrieved successfully",
  "data": {},
  "timestamp": "2026-08-27T10:30:00Z"
}
```

---

## 1. Authentication & Security Endpoints (`/api/auth`)

### POST `/api/auth/login`
Authenticates user credentials and returns a signed JWT access token.
- **Request Body**:
  ```json
  {
    "username": "admin@hrplatform.com",
    "password": "Password123!"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin@hrplatform.com",
      "email": "admin@hrplatform.com",
      "role": "Admin",
      "employee_id": 1
    }
  }
  ```

### GET `/api/auth/me`
Retrieves current authenticated user session details.

---

## 2. Department & Employee Directory (`/api/employees`, `/api/departments`)

### GET `/api/departments/`
Returns all active organizational departments.

### GET `/api/employees/`
Retrieves paginated employee directory list with optional search and department filter queries.

---

## 3. Talent Acquisition & ATS Endpoints (`/api/jobs`, `/api/candidates`, `/api/applications`)

### POST `/api/jobs/`
Creates a new job posting requisition.
- **Request Body**:
  ```json
  {
    "title": "Senior Backend Engineer",
    "department_id": 1,
    "position_level": "Senior",
    "employment_type": "Full Time",
    "location": "Bengaluru, India",
    "experience_years_min": 5,
    "experience_years_max": 8,
    "salary_min": 1800000.0,
    "salary_max": 2500000.0,
    "description": "We are seeking a Senior Python/Flask Engineer...",
    "requirements": "Python, Flask, PostgreSQL, Docker, Redis"
  }
  ```

### POST `/api/applications/`
Submits a job application for a candidate.

### POST `/api/matching/match-score`
Computes TF-IDF similarity score between candidate profile and job requirements.

---

## 4. Attendance & Leave Endpoints (`/api/attendances`, `/api/leaves`)

### POST `/api/attendances/check-in`
Logs daily employee check-in timestamp.

### POST `/api/leaves/`
Submits a new leave request application.

---

## 5. Payroll & Compensation Endpoints (`/api/payroll`)

### POST `/api/payroll/process-run`
Executes monthly payroll processing for specified month and year.

### GET `/api/payroll/payslips/<int:payslip_id>`
Retrieves individual payslip itemization breakdown.

---

## 6. Asset & IT Management Endpoints (`/api/assets`)

### GET `/api/assets/`
Retrieves hardware asset inventory directory.

### POST `/api/assets/assignments`
Assigns a hardware asset item to an employee.

---

## 7. Onboarding & Exit Clearance Endpoints (`/api/lifecycle`)

### GET `/api/lifecycle/checklists/<int:employee_id>`
Retrieves onboarding checklist tasks for an employee.

### POST `/api/lifecycle/clearances/<int:clearance_id>/clear`
Signs off departmental exit clearance line item.

---

## 8. OKRs & Performance Endpoints (`/api/okrs`)

### POST `/api/okrs/objectives`
Creates a new cascading OKR objective.

---

## 9. Learning Management (LXP) Endpoints (`/api/learning`)

### GET `/api/learning/courses`
Returns LXP course catalog directory.

---

## 10. Timesheets & Shifts Endpoints (`/api/timesheets`)

### POST `/api/timesheets/weekly`
Submits weekly timesheet work log.

---

## 11. Expenses & Travel Endpoints (`/api/expenses`)

### POST `/api/expenses/claims`
Submits a new reimbursement expense claim.

---

## 12. Compliance & Grievances Endpoints (`/api/compliance`)

### POST `/api/compliance/grievances`
Files a confidential grievance ticket.

---

## 13. Workforce Analytics Endpoints (`/api/workforce`)

### GET `/api/workforce/headcount-plans`
Retrieves department headcount planning targets.
