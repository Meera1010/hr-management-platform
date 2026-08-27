# Job Application Module

## Overview

The Job Application Management module enables the AI-Powered HR Platform to receive, track, and manage candidate applications for open jobs. It links fictional Candidates to fictional Jobs via an `Application` model.

## Features

- **Candidate Side**:
  - View Open Jobs
  - Apply for a job (one application per job) with an optional cover letter.
  - View all submitted applications and their current statuses.
  - Withdraw an application if it is not yet final (e.g., Selected or Rejected).

- **HR / Recruiter Side**:
  - View all applications across all jobs with pagination.
  - Search applications by Job Title, Candidate Name, or Application Code.
  - Filter applications by Status.
  - Update Application Statuses (Submitted -> Under Review -> Shortlisted -> Selected/Rejected).
  - Add internal Recruiter Notes that candidates cannot see.

## Data Safety Rules

In accordance with strict educational demo constraints:
- NO real personal data is collected or seeded.
- Applications belong to fictional candidates.
- Recruiter notes contain generic placeholder text.

## API Endpoints

- `POST /api/applications`: Create a new application.
- `GET /api/applications`: Fetch applications (with RBAC visibility rules).
- `GET /api/applications/<id>`: Get details for one application.
- `PATCH /api/applications/<id>/status`: Update status and notes (HR/Recruiter only).
- `DELETE /api/applications/<id>`: Withdraw application (Candidate only).

## Technical Implementation

- Uses SQLAlchemy `UniqueConstraint` on `candidate_id` + `job_id` to prevent duplicate applications.
- Integrated deeply with the RBAC `role_required` decorators.
- Frontend uses React and React Bootstrap with components split between candidate self-service (`CandidateApplications.jsx`) and recruiter management (`RecruiterApplications.jsx`).
