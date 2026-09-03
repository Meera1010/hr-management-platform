# AI-Powered HR, Recruitment & Employee Management Platform

A comprehensive, production-grade enterprise web application built for modern HR operations, talent acquisition, employee self-service, performance reviews, training management, and AI-driven candidate ranking and career recommendations.

> **DATA PRIVACY & SAFETY COMPLIANCE:**
> All data in this platform is 100% fictional/demo data. No real personal information (such as Aadhaar, PAN, Passport, Bank details, Medical records, or Biometrics) is stored or used. Candidate ranking and career matching strictly evaluate professional qualifications (skills, experience, education) and NEVER evaluate sensitive demographic factors (gender, religion, caste, race, age, medical status, marital status, or financial background). All AI features serve purely as decision-support tools.

---

## Architecture & Technology Stack

- **Frontend:** React 18, React Router v7, React Bootstrap 5, Vite, Vanilla CSS & Glassmorphism design system.
- **Backend:** Python 3.7+, Flask 2.x, Flask-SQLAlchemy, Flask-JWT-Extended, PostgreSQL (Neon cloud) via `psycopg2`.
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
- A PostgreSQL database (the app is configured for a Neon cloud DB by default)

### Quick Start (Windows, recommended)
Run these two batch scripts in two separate terminals (backend must be running before the frontend):

```bash
# Terminal 1 - backend (installs deps, tests Neon connection, seeds DB, starts server)
setup_and_run.bat

# Terminal 2 - frontend (installs deps and starts Vite dev server)
start_frontend.bat
```

Then open `http://localhost:5173`.

### Backend Setup (manual)
```bash
cd backend

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows

# Install dependencies (includes psycopg2-binary for PostgreSQL)
pip install -r requirements.txt

# Test the Neon PostgreSQL connection (must print "CONNECTION OK")
python test_db_connection.py

# Create tables & seed database with fictional demo data
python seed.py

# Run the Flask backend API server (runs on http://localhost:5001)
python run.py
```

### Database Configuration
The app connects to **PostgreSQL** by default. Set the connection string in `backend/.env`:

```
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
```

A Neon cloud connection string is pre-configured in `backend/.env`. If you prefer SQLite for local-only development, set `DATABASE_URL=sqlite:///../../database/hr_platform.db`.

### Frontend Setup (manual)
```bash
cd frontend
npm install
npm run start   # starts Vite dev server on http://localhost:5173
# or
npm run build   # build for production
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

---

## Troubleshooting

### Blank / white page in the browser
- **Hard refresh** (Ctrl+Shift+R) to clear the stale cached bundle.
- Make sure the **frontend** (`npm run dev`, port 5173) and **backend** (`python run.py`, port 5001) are both running.
- Bootstrap is bundled locally now (no CDN dependency), so the UI renders even offline.
- Open **DevTools → Console**. If you see a red `TypeError`, note the `file:line` it points to and report it.

### Backend "not working" / module not found
- Ensure the venv is active and the Postgres driver is installed:
  `pip install psycopg2-binary`
- Run `python test_db_connection.py` — it must print `CONNECTION OK`. If it errors, the DB URL or network is wrong.

### Can't log in after switching to PostgreSQL
- The Postgres tables start empty. Run `python seed.py` **once** to create tables and demo users (creates roles + `admin@example.com` etc.). The seed is idempotent, so re-running it is safe.

### Port already in use
- Change the backend port in `backend/.env` (`PORT=5001`) or the frontend; ensure nothing else is using 5173/5001.

### CORS / API requests failing in the frontend
- Frontend calls `http://localhost:5001/api` — confirm that matches your backend port.
- `CORS_ORIGINS` in `backend/.env` must include `http://localhost:5173`.
