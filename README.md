# AI-Powered HR, Recruitment & Employee Management Platform

A comprehensive, production-grade enterprise web application built for modern HR operations, talent acquisition, employee self-service, performance reviews, training management, and AI-driven candidate ranking and career recommendations.

> **DATA PRIVACY & SAFETY COMPLIANCE:**
> All data in this platform is 100% fictional/demo data. No real personal information (such as Aadhaar, PAN, Passport, Bank details, Medical records, or Biometrics) is stored or used. Candidate ranking and career matching strictly evaluate professional qualifications (skills, experience, education) and NEVER evaluate sensitive demographic factors (gender, religion, caste, race, age, medical status, marital status, or financial background). All AI features serve purely as decision-support tools.

---

## Architecture & Technology Stack

- **Frontend:** React 18, React Router v7, React Bootstrap 5, Vite, Vanilla CSS & Glassmorphism design system.
- **Backend:** Python 3.7+, Flask 2.x, Flask-SQLAlchemy, Flask-JWT-Extended, SQLite.
- **Security & Authentication:** JWT bearer tokens, password hashing via werkzeug, Role-Based Access Control (RBAC) across 6 distinct roles (`Admin`, `HR`, `Recruiter`, `Employee`, `Candidate`, `Interviewer`).
- **AI & Analytics Engine:** Keyword skill extraction, rule-based resume parsing, TF-IDF / heuristic candidate matching score calculation, transparent decision-support career recommendation algorithms.

---

## Core Modules & Features

1. **Authentication & RBAC**: Secure JWT-based authentication with role-scoped navigation and endpoint protection for 6 system roles.
2. **Department & Employee Management**: Complete employee lifecycle management, department directory, designation tracking, employment types, and staff onboarding.
3. **Jobs & Career Openings**: Job creation, draft/publish/close/archive workflows, location filtering, and public candidate job portal.
4. **Candidate Management & Applications**: Candidate profile tracking, resume uploading, application submission, status progression, and recruiter notes.
5. **Resume Parsing & Skill Extraction**: Text extraction, automatic skill tagging against standard taxonomy, and candidate profile enrichment.
6. **AI Candidate Matching & Ranking**: Multivariable job-candidate match percentage scoring (0-100%), skill overlap analysis, and recruiter ranking dashboards.
7. **Interview Management**: Technical, HR, and managerial interview scheduling, candidate notifications, and multi-criteria feedback scoring.
8. **Offer Management**: Offer letter package creation, salary specification, approval status tracking, candidate accept/decline actions, and auto-status updates.
9. **Attendance & Time Tracking**: Employee check-in/check-out, work-hours calculation, WFH/Half Day status logging, and HR attendance monitoring.
10. **Leave Management**: Leave requests (Casual, Annual, Sick, Unpaid), manager approval/rejection workflows, and leave balance tracking.
11. **Performance Reviews**: Multi-metric evaluation (Productivity, Quality, Teamwork, Goal score), overall score computation, review period tracking, and feedback.
12. **Training & Skill Development**: Course catalog creation, employee training assignments, due dates, employee completion submission, and score tracking.
13. **In-App Notifications**: Real-time notification bell dropdown with unread badge counter, system event triggers, mark-as-read, and notifications center.
14. **Role-Specific Dashboards**: Custom metrics overview and quick actions tailored for Admin, HR, Recruiter, Employee, and Candidate roles.
15. **HR & Recruitment Analytics**: Interactive analytics overview covering the complete recruitment funnel, department headcount distribution, employment composition, and leave utilization.
16. **Executive Reports & CSV Export**: Report generator interface with formatted tables and instant 1-click CSV export for Headcount, Attendance, Recruitment, and Performance.
17. **Global Multi-Entity Search**: Multi-category instant search across Employees, Candidates, Jobs, Applications, and Departments.
18. **Career Recommendations**: Personalized career growth recommendations matching Candidate/Employee skills against active job requirements with missing skill gap analysis.

---

## Getting Started & Installation

### Prerequisites
- Python 3.7+
- Node.js 18+ and npm

### Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create & activate virtual environment (optional)
python -m venv venv
venv\Scripts\activate # On Windows

# Install dependencies
pip install -r requirements.txt

# Initialize & seed database with fictional demo data
python seed.py

# Run the Flask backend API server (runs on http://localhost:5001)
python run.py
```

### Frontend Setup
```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Run the Vite development server (runs on http://localhost:5173)
npm run start

# Or build for production
npm run build
```

---

## Testing & Quality Assurance

```bash
# Run backend test suite (82 automated pytest cases)
cd backend
python -m pytest

# Run frontend build check
cd frontend
npm run build
```

---

## Demo Credentials (Role-Based Access)

| Role | Email | Password | Allowed Access |
|---|---|---|---|
| **Admin** | `admin@example.com` | `demo-password` | Full system administration, User & Role management, HR & Recruiter tools |
| **HR** | `hr@example.com` | `demo-password` | Departments, Employees, Offers, Training, Analytics, Reports, Performance |
| **Recruiter** | `recruiter@example.com` | `demo-password` | Jobs, Candidates, Applications, Resumes, AI Rankings, Interviews |
| **Employee** | `employee@example.com` | `demo-password` | Self-service attendance, Leaves, My Training, Internal Careers, AI Growth |
| **Candidate** | `candidate@example.com` | `demo-password` | Job search, Applications, My Resumes, Interviews, My Offers, AI Job Matches |
| **Interviewer** | `interviewer@example.com` | `demo-password` | Assigned interview list, Candidate evaluation & feedback forms |

---

## Actual Lines of Code (LOC) Report

Calculated using `count_loc.py` (excluding `node_modules`, `.git`, virtual environments, cache, compiled bundles, database files, binary assets, blank lines, and comments):

```
========================================
      ACTUAL LINES OF CODE (LOC) REPORT
========================================
Backend LOC         :    4,533
Frontend LOC        :    7,645
Tests LOC           :    1,893
Utilities LOC       :      534
Configuration LOC   :        9
Documentation LOC   :      255
TOTAL LOC           :   14,869
========================================
```
"# hr-management-platform" 
