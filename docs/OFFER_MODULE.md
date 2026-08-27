# Offer Management Module

## Overview

The Offer Management module allows HR managers to create, send, and track job offers for selected candidates. Candidates can accept or decline offers through their portal.

## Features

- Create offers with salary, start date, and expiration date
- Status workflow: Draft → Sent → Accepted / Declined / Expired / Cancelled
- Date validation (expiration cannot precede start date)
- Candidate self-service: Accept or Decline sent offers
- Accepting an offer automatically updates the Application status to "Selected"

## Model: Offer
| Field | Type | Description |
|---|---|---|
| `offer_code` | String | Unique code (OFF-0001) |
| `application_id` | Integer | FK to Application |
| `job_title` | String | Offered job title |
| `employment_type` | String | Full Time / Part Time / Contract / Internship |
| `offered_salary` | String | Demo salary string (e.g., "$85,000 / year") |
| `start_date` | String | YYYY-MM-DD |
| `expiration_date` | String | YYYY-MM-DD |
| `status` | String | Draft / Sent / Accepted / Declined / Expired / Cancelled |
| `notes` | Text | Additional offer details |

## API Endpoints

| Method | Endpoint | Roles | Description |
|---|---|---|---|
| GET | `/api/offers` | Admin, HR, Recruiter, Candidate | List offers (role-filtered) |
| GET | `/api/offers/<id>` | Admin, HR, Recruiter, Candidate | Get single offer |
| POST | `/api/offers` | Admin, HR | Create offer |
| PUT | `/api/offers/<id>` | Admin, HR | Update offer |
| PATCH | `/api/offers/<id>/status` | Admin, HR | Update offer status |
| DELETE | `/api/offers/<id>` | Admin, HR | Delete offer |
| POST | `/api/offers/<id>/accept` | Candidate | Accept a sent offer |
| POST | `/api/offers/<id>/decline` | Candidate | Decline a sent offer |

## Status Workflow

```
Draft ──→ Sent ──→ Accepted
               └──→ Declined
               └──→ Expired
     └──→ Cancelled
```

## Data Safety

- Salary values use demo-safe strings like "$85,000 / year"
- No real personal financial information is stored
- All offer data uses fictional demo candidates and jobs

## Frontend Pages

| Route | File | Role |
|---|---|---|
| `/hr/offers` | `HROffers.jsx` | HR, Admin |
| `/candidate/offers` | `CandidateOffers.jsx` | Candidate |
