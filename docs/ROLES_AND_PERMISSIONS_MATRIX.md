# Roles & Authorization Matrix Documentation

## Overview
This document specifies the Security Architecture, Token Validation Rules, Access Scopes, and Role-Based Authorization Matrix for the **AI HR Platform**.

---

## 1. System Roles Summary

1. **Admin**: System Administrator with uninhibited CRUD access across all operational modules, user account management, role definitions, and audit logs.
2. **HR**: Human Resources Specialist with administrative access to department directories, employee profiles, payroll runs, onboarding checklists, exit clearances, OKRs, training, analytics, and executive reports.
3. **Recruiter**: Talent Acquisition Specialist managing job requisitions, candidate pools, application pipelines, AI resume match rankings, and interview schedules.
4. **Employee**: Self-service user account with access to attendance check-in/out, leave requests, payslip viewing, assigned IT assets, LXP learning courses, timesheets, expense claims, and internal career growth recommendations.
5. **Candidate**: Job applicant account with access to the public career portal, job application submissions, resume management, interview invitations, and offer letter acceptance.
6. **Interviewer**: Technical & Managerial evaluator with access to assigned candidate evaluation scorecards and feedback forms.

---

## 2. Endpoint Authorization Rulebook

```
+------------------------------------+---------------------------------------+
| Route Prefix                       | Allowed System Roles                  |
+------------------------------------+---------------------------------------+
| /api/auth/                         | Public (Login), All Authenticated     |
| /api/users/                        | Admin                                 |
| /api/roles/                        | Admin                                 |
| /api/departments/                  | Admin, HR                             |
| /api/employees/                    | Admin, HR                             |
| /api/jobs/                         | Admin, HR, Recruiter, Employee, Cand. |
| /api/candidates/                   | Admin, HR, Recruiter, Candidate       |
| /api/applications/                 | Admin, HR, Recruiter, Candidate       |
| /api/resumes/                      | Admin, HR, Recruiter, Candidate       |
| /api/interviews/                   | Admin, HR, Recruiter, Interviewer     |
| /api/offers/                       | Admin, HR, Candidate                  |
| /api/payroll/                      | Admin, HR, Employee (Self)            |
| /api/assets/                       | Admin, HR, Employee (Self)            |
| /api/lifecycle/                    | Admin, HR, Employee (Self)            |
| /api/okrs/                         | Admin, HR, Employee (Self)            |
| /api/learning/                     | Admin, HR, Employee (Self)            |
| /api/timesheets/                   | Admin, HR, Employee (Self)            |
| /api/expenses/                     | Admin, HR, Employee (Self)            |
| /api/compliance/                   | Admin, HR, Employee (Self)            |
| /api/workforce/                    | Admin, HR                             |
+------------------------------------+---------------------------------------+
```
