# Enterprise System Architecture & Infrastructure Blueprint

## Executive Summary
This document specifies the end-to-end multi-layer software architecture, system boundaries, security topology, entity relational schemas, business logic engines, API integration contracts, background task processing, and client presentation design system of the **AI-Powered HR, Recruitment & Employee Management Platform**.

---

## 1. System Context & High-Level Architecture Topology

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT PRESENTATION LAYER                         |
|  +-----------------------------------------------------------------------------+  |
|  | Single Page Application (SPA): React 18, React Router v7, React Bootstrap 5  |  |
|  | State & Auth Context: JWT Bearer Tokens, Axios Interceptors                 |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                  HTTPS / REST API
                                         v
+-----------------------------------------------------------------------------------+
|                                 APPLICATION BACKEND LAYER                         |
|  +-----------------------------------------------------------------------------+  |
|  | Flask Application Server & Blueprint Router (25 Functional Sub-Systems)      |  |
|  +-----------------------------------------------------------------------------+  |
|  | Business Logic & Analytical Engines:                                         |  |
|  |  - Payroll & Tax Calculator (Old vs New Regime, TDS, 80C/80D/24B)            |  |
|  |  - Candidate-Job AI Matching Engine (Vector TF-IDF Similarity Scoring)      |  |
|  |  - Asset Procurement & Depreciation Engine (SLM & WDV Schedules)           |  |
|  |  - Full & Final (FnF) Clearance Engine (Gratuity Act & Leave Encashment)   |  |
|  |  - OKR Progress Alignment & 360-Degree Feedback Competency Radar           |  |
|  |  - LXP Quiz Grading & Certification Engine                                  |  |
|  |  - Timesheet Overtime Premium Calculator (1.5x / 2.0x Rates)               |  |
|  |  - Predictive Workforce Attrition Risk & Compa-Ratio Benchmark Engine      |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                 SQLAlchemy ORM
                                         v
+-----------------------------------------------------------------------------------+
|                                 PERSISTENCE & STORAGE LAYER                       |
|  +-----------------------------------------------------------------------------+  |
|  | Relational Database: SQLite / PostgreSQL (34 Normalized Entity Tables)        |  |
|  | Document File Store: Resume PDF/DOCX Attachments & Expense Receipt Scans      |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Functional Sub-Systems Specification

### Sub-System 1: Authentication & Role-Based Access Control (RBAC)
- **Authentication Protocol**: Stateless JSON Web Token (JWT) with HMAC-SHA256 signature verification.
- **Roles Matrix**:
  - `Admin`: Uninhibited CRUD permissions across all system resources.
  - `HR`: Administrative management of personnel, payroll, lifecycle, OKRs, LXP, and workforce planning.
  - `Recruiter`: Requisition posting, candidate sourcing, resume parsing, match scoring, and interview scheduling.
  - `Employee`: Self-service portal for attendance, leaves, payslips, assets, timesheets, and expense claims.
  - `Candidate`: Public portal for job browsing, resume upload, and application tracking.
  - `Interviewer`: Access to evaluation scorecards and candidate feedback.

### Sub-System 2: Candidate Sourcing & Recruitment ATS Pipeline
- **Job Requisitions**: Departmental budgeting, position level (Entry, Mid, Senior, Executive), employment type, location, experience range, and active status tracking.
- **Candidate Database**: Centralized talent pool storing personal contact details, current employer, notice period, expected CTC, primary skill tags, and resume document attachments.
- **Application Tracking System (ATS)**: Multi-stage hiring workflow transitions:
  1. `Applied`
  2. `Shortlisted`
  3. `Screening`
  4. `Interview Scheduled`
  5. `Feedback Submitted`
  6. `Offered`
  7. `Accepted`
  8. `Hired`
  9. `Rejected`
  10. `Withdrawn`

---

### Sub-System 3: AI Resume Parsing & Candidate-Job Matching
- **TF-IDF & Cosine Similarity Engine**: Computes normalized text similarity vector scores between candidate resume text/skills and job requirements.
- **Recruiter Candidate Ranking**: Automatically ranks applicant pools based on match percentage, experience alignment, and notice period suitability.
- **Match Score Explanation**: Generates readable rationale highlighting matching skill keywords and identifying missing skill requirements.

---

### Sub-System 4: Offer Letter Package & Compensation Benchmarking
- **Offer Package Generator**: Computes proposed CTC, Basic Pay, HRA, Special Allowances, Joining Bonus, Stocks/ESOPs, proposed designation, joining date, and offer expiration date.
- **Candidate Decision Workflow**: Candidate login portal to review downloadable PDF offer terms and submit binding Accept or Decline decisions.

---

### Sub-System 5: Payroll & Indian Income Tax Calculation Engine
- **Salary Structures**: Configurable pay bands allocating CTC percentages across Basic Pay (40%), HRA (20%), Special Allowance (20%), and Employer PF (12%).
- **Tax Regimes**:
  - **New Tax Regime (FY 2026-2027)**: Tax slabs (0-3L Nil, 3-7L 5%, 7-10L 10%, 10-12L 15%, 12-15L 20%, >15L 30%) with Section 87A rebate up to ₹25,000 for taxable income <= 7.0 Lakhs. Standard deduction: ₹75,000.
  - **Old Tax Regime**: Standard deduction ₹50,000 with investment exemptions: Section 80C (PPF, ELSS, EPF, LIC up to ₹1,50,000), Section 80D (Health Insurance up to ₹75,000), Section 24B (Home Loan Interest up to ₹2,00,000), and HRA Exemption.
- **Monthly TDS Schedule**: Automatically calculates monthly Tax Deduction at Source (TDS) schedules based on employee annual investment declarations.
- **Bank Batch Payout Export**: Exports corporate payout files in HDFC CMS CSV, ICICI CIB text, and SBI Corporate Formats.

---

### Sub-System 6: Hardware Asset & IT Inventory Management
- **Asset Lifecycle**: Barcode asset tag tracking, hardware categories (Laptops, Monitors, Mobile Devices, Accessories), serial numbers, purchase cost, vendor details, warranty expiry dates, and asset status (`Available`, `Assigned`, `Under Maintenance`, `Decommissioned`).
- **Assignment & Return Workflow**: Assigns IT hardware to active employees with digital receipt signatures and condition logs on return.
- **IT Support Tickets**: Ticketing system for hardware repairs, software installation requests, and display replacement support.

---

### Sub-System 7: Onboarding & Resignation Exit Clearance (FnF)
- **Onboarding Checklists**: Automatically assigns orientation tasks across IT Setup, HR Documentation, Finance Bank Account Linking, and Security Badge Issuance.
- **Resignation Notice Period Compliance**: Tracks requested last working day against required notice period (60 days standard), calculating notice shortfall recovery days.
- **Multi-Department Exit Clearance**: 5-department clearance matrix (IT Assets, Finance Dues, Admin Library, HR Records, Security Access Keycards).
- **Full & Final (FnF) Financial Settlement**:
  - **Gratuity Act Formula**: `(15 * Basic Salary * Tenure Years) / 26` for continuous service >= 4.8 years.
  - **Leave Encashment**: `(Basic Salary / 30) * Unavailed Earned Leave Days`.
  - **Net Settlement Payout**: `Earned Unpaid Days Pay + Gratuity + Leave Encashment - Notice Shortfall Recovery - Outstanding Dues`.

---

### Sub-System 8: OKRs & 360-Degree Performance Reviews
- **Quarterly OKRs**: Cascading objectives across Company, Department, and Individual levels with weighted Key Results.
- **Automatic Progress Recalculation**: Key result metric progress updates trigger objective percentage completion recalculations.
- **360-Degree Review Radar Matrix**: Evaluates performance across 4 core competencies: Leadership, Technical Skill, Communication, and Teamwork.
- **Performance Improvement Plans (PIP)**: 30/60/90-day structured intervention plans with target milestones.

---

### Sub-System 9: Learning Experience Platform (LXP)
- **Course Catalog**: Internal academy courses categorized under Technical, Soft Skills, Leadership, Compliance, and Security.
- **Quiz Grading & Certificates**: Automated quiz scoring, passing grade verification (70%), and tamper-evident certificate issuance with unique verification codes.
- **Skill Gap Matrix**: Identifies departmental missing skills and recommends appropriate internal LXP courses.

---

### Sub-System 10: Timesheets & Shift Rosters
- **Weekly Project Timesheet**: Logs daily project work hours, task descriptions, and billable status.
- **Overtime Premium Engine**: Computes overtime payouts using 1.5x multiplier for weekday OT and 2.0x multiplier for weekend/holiday OT.
- **Shift Rostering & Swaps**: Weekly shift assignment schedules (Morning 9am-6pm, Evening 2pm-11pm, Night 10pm-7am) with shift swap request workflows.

---

### Sub-System 11: Expense Reimbursements & Business Travel
- **Expense Claims**: Itemized reimbursement requests with proof of receipt attachments and category policy limit auditing.
- **Travel Pre-Approvals**: Domestic & international business travel requests with per-diem calculations.

---

### Sub-System 12: Grievance Redressal & Audit Logging
- **Confidential Grievance Reporting**: Anonymous or identified grievance ticket submission with SLA target resolution timers.
- **Audit Logs**: Immutable activity logging capturing user ID, action, target entity, timestamp, IP address, and JSON diffs of modified fields.

---

### Sub-System 13: Predictive Workforce Analytics & Headcount Planning
- **Flight-Risk Attrition Evaluation**: Evaluates employee tenure, compensation competitiveness, review scores, and absenteeism to calculate attrition probability.
- **Compa-Ratio Benchmark**: Measures employee salary against market median pay benchmarks (`Compa-Ratio = Salary / Market Benchmark`).
