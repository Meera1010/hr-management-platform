# Testing, QA & Verification Suite Documentation

## Overview
This document specifies the Quality Assurance strategy, Automated Unit & Integration Testing methodology, Pytest Test Suite topology, and Frontend Build Verification procedures for the **AI HR Platform**.

---

## 1. Test Suite Topology & Directory Map

The platform maintains 24 comprehensive automated Pytest test suites covering 156+ test cases across all backend sub-systems and utility calculation engines:

```
backend/tests/
├── conftest.py                       # Fixtures for Flask test client & JWT auth headers
├── test_applications.py              # Candidate application creation, status transitions, applicant viewing
├── test_asset_depreciation_models.py # SLM/WDV hardware depreciation schedules & warranty expirations
├── test_assets.py                    # IT hardware inventory, category creation, asset assignments
├── test_assets_advanced.py           # Software licenses, IT support ticket logging, return condition logs
├── test_attendance.py                # Employee check-in/out, duplicate punch prevention, monthly summaries
├── test_auth.py                      # User login, invalid credentials, password change, /me token endpoint
├── test_candidates.py                # Candidate profile creation, search filters, recruiter RBAC scope
├── test_compliance.py                # Confidential grievance submission, policy listing, audit logs
├── test_compliance_advanced.py       # Policy digital signatures & audit log delta serialization
├── test_compliance_sla_escalation.py # Grievance SLA resolution targets by severity
├── test_dashboards_analytics.py      # Admin dashboard stats, executive analytics overview, CSV exports
├── test_departments.py               # Department CRUD operations, unique code enforcement
├── test_employees.py                 # Employee directory CRUD, code generation, search filters
├── test_exit_settlement_formulas.py # Gratuity Act formula, leave encashment, notice pay recovery
├── test_expense_audit_rules.py       # Expense policy limit auditing & missing receipt proof flags
├── test_expenses.py                  # Reimbursement claims submission, travel requests, manager approvals
├── test_expenses_advanced.py         # Multi-currency expense conversions & per-diem calculations
├── test_interviews.py                # Interview round scheduling, conflict checking, scorecard ratings
├── test_jobs.py                      # Job requisition CRUD, open status filtering, recruiter access
├── test_learning.py                  # LXP course catalog, course module listing, employee enrollments
├── test_learning_advanced.py         # Quiz attempts grading, 70% passing threshold, certificate generation
├── test_leaves.py                    # Leave request applications, date validation, manager approvals
├── test_lxp_quiz_grading.py          # Skill matrix gap analysis & course recommendation matching
├── test_matching.py                  # TF-IDF candidate-job match scoring & similarity calculations
├── test_notifications.py             # User real-time notification listing & unread mark toggles
├── test_offers.py                    # Offer letter package creation, candidate accept/decline workflow
├── test_okr_progress_rules.py        # Department OKR progress aggregation & 360 feedback radar scores
├── test_okrs.py                      # Objective creation, key result progress updates, OKR recalculations
├── test_okrs_advanced.py             # Review cycle schedules, 360 review feedback submission, PIP plans
├── test_onboarding_exit.py           # Onboarding checklist initiation, task completion toggles
├── test_onboarding_exit_advanced.py  # Resignation notice period calculations, 5-dept clearance matrix
├── test_payroll.py                   # Salary structure configuration, employee CTC assignment
├── test_payroll_advanced.py          # Monthly payroll run execution, payslip generation, tax declarations
├── test_payroll_tax_slabs.py         # Old vs New tax regime slabs, TDS schedules, bank CMS payout export
├── test_performance.py              # Performance review creation, rating validation, manager scorecards
├── test_ranking.py                   # Candidate ranker scoring formula & recruiter candidate ranking API
├── test_resumes.py                   # Resume file upload, text extraction, resume download & deletion
├── test_timesheet_overtime_payouts.py# Weekday 1.5x / Weekend 2.0x overtime payouts & billable utilization
├── test_timesheets.py                # Weekly timesheet submission, shift rosters, overtime claims
├── test_training.py                 # Training course assignment & completion status updates
├── test_utility_engines.py           # Compliance rule checker, skill gap matrix, time tracking calculator
└── test_workforce.py                # Headcount planning targets, flight-risk evaluations, compa-ratios
```

---

## 2. Automated Test Execution Commands

### Execute All Pytest Test Suites
```bash
cd backend
python -m pytest
```

### Execute Specific Sub-System Test
```bash
python -m pytest tests/test_payroll_tax_slabs.py
```

### Execute Frontend Production Build Validation
```bash
cd frontend
npm run build
```
