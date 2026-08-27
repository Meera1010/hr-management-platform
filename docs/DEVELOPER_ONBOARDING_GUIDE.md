# Full-Stack Developer Onboarding & Contribution Guide

## Overview
Welcome to the development team of the **AI-Powered HR, Recruitment & Employee Management Platform**! This guide details local environment setup, project architecture conventions, coding practices, testing workflows, and deployment procedures.

---

## 1. Prerequisites & Tooling Setup
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Python**: v3.7.0 or higher
- **Git**: v2.30.0 or higher

---

## 2. Repository Architecture & Directory Tree

```
AI-HR-Platform/
├── backend/
│   ├── app/
│   │   ├── models/         # 15 SQLAlchemy model files (34 tables)
│   │   ├── routes/         # 25 Flask Blueprint API route handlers
│   │   ├── services/       # Business logic engines & service calculators
│   │   ├── utils/          # Financial math, exporters, auth & audit helpers
│   │   ├── config.py       # Application environment settings
│   │   └── __init__.py     # Flask factory & blueprint registration
│   ├── tests/              # 18 Pytest test suites (132+ test cases)
│   ├── seed.py             # Base fictional data seeder
│   ├── append_seed.py      # Enterprise sub-systems data seeder
│   └── run.py              # Backend entrypoint server
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable layout & UI components
│   │   ├── context/        # AuthContext JWT authentication provider
│   │   ├── pages/          # 35 React page modules (HR, Recruiter, LXP, Payroll)
│   │   ├── services/       # Axios API integration clients
│   │   └── App.jsx         # React Router v7 routes & navigation bar
│   ├── package.json        # Frontend dependencies & build scripts
│   └── vite.config.js      # Vite build configuration
├── docs/                   # 15 Comprehensive technical reference manuals
└── count_loc.py            # Automated Lines of Code (LOC) counter
```

---

## 3. Local Development Quickstart

### Step A: Backend Environment Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python seed.py
python append_seed.py
python run.py
```
*The Flask API backend will start listening on `http://localhost:5001`.*

### Step B: Frontend Setup
```bash
cd frontend
npm install
npm run start
```
*The Vite development server will open on `http://localhost:5173`.*

---

## 4. Code Standards & Testing Conventions

### Automated Test Execution
```bash
# Run full pytest suite
cd backend
python -m pytest

# Run frontend build validation
cd frontend
npm run build
```

### Git Commit Guidelines
- Use descriptive commit messages following Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- Always ensure backend unit tests pass 100% before committing.
