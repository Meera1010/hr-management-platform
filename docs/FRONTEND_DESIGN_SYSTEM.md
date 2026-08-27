# Frontend Design System & Component Library Guidelines

## Overview
The frontend of the **AI HR Platform** is built using React 18, React Router v7, React Bootstrap 5, Vite, and Vanilla CSS with modern Glassmorphism aesthetics, dynamic dark modes, micro-animations, and full responsive design.

---

## 1. Color Palette & Aesthetics Tokens

### Primary Palette
- **Primary Indigo**: `#4f46e5`
- **Secondary Slate**: `#64748b`
- **Success Emerald**: `#10b981`
- **Warning Amber**: `#f59e0b`
- **Danger Rose**: `#f43f5e`
- **Dark Obsidian**: `#0f172a`
- **Light Surface**: `#f8fafc`

### Glassmorphism Tokens
- **Backdrop Blur**: `backdrop-filter: blur(12px);`
- **Glass Border**: `border: 1px solid rgba(255, 255, 255, 0.18);`
- **Glass Background**: `background: rgba(255, 255, 255, 0.75);`

---

## 2. Shared Component Architecture

### Layout Wrappers
- `<Navigation />`: Sticky top navigation header with user role indicator, global multi-entity search input, and real-time notification dropdown.
- `<ProtectedRoute />`: Role-based authorization wrapper enforcing allowed roles before rendering nested page components.

### Page Components Directory (`frontend/src/pages/`)
1. `Users.jsx` & `Roles.jsx`: User administration & role permissions.
2. `Departments.jsx` & `Employees.jsx`: Organizational directory & staff profiles.
3. `jobs/`: Job creation, editing, profile views, and candidate search portal.
4. `candidates/`: Candidate management & self-service profile builder.
5. `applications/`: Recruiter applicant tracking pipeline & candidate applications.
6. `resumes/`: AI resume parsing & skill tagging dashboard.
7. `matching/` & `recruiter/`: Candidate-job match percentage scoring & AI recruiter ranking.
8. `hr/`: Offer letter package generator.
9. `payroll/`: Salary structure config, monthly payroll runs, payslips, and tax declarations.
10. `assets/`: IT hardware inventory, serial numbers, assignments, and support tickets.
11. `lifecycle/`: Onboarding orientation checklists and resignation exit clearance workflows.
12. `okrs/`: Quarterly OKR progress tracking & 360-degree performance reviews.
13. `learning/`: LXP course catalog, quiz player, and certificate viewer.
14. `timesheets/`: Weekly project timesheet logging & shift rosters.
15. `expenses/`: Reimbursement claims & business travel pre-approvals.
16. `compliance/`: Confidential grievance reporting & company policy documents.
17. `workforce/`: Headcount forecasting, flight-risk analytics, and salary benchmarks.
