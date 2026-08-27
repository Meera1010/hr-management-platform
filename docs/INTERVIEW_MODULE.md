# Interview Management Module

## Overview

The Interview Management module allows Recruiters and HR managers to schedule, track, and evaluate candidate interviews end-to-end.

## Features

- Schedule interviews with conflict detection (same interviewer, date, and time)
- Multiple interview types: Technical, HR, Managerial, General, Panel
- Status tracking: Scheduled → Completed / Cancelled / Rescheduled
- Interview feedback with per-dimension scoring
- Candidate view of their own interviews (without internal notes)

## Models

### Interview
| Field | Type | Description |
|---|---|---|
| `interview_code` | String | Unique code (INT-0001) |
| `application_id` | Integer | FK to Application |
| `interviewer_name` | String | Demo interviewer name |
| `interview_type` | String | Technical / HR / Managerial / General |
| `scheduled_date` | String | YYYY-MM-DD |
| `scheduled_time` | String | HH:MM |
| `duration_minutes` | Integer | Duration in minutes |
| `meeting_link` | String | Demo meeting URL |
| `status` | String | Scheduled / Completed / Cancelled / Rescheduled |
| `notes` | Text | Internal notes (hidden from candidates) |

### InterviewFeedback
| Field | Type | Description |
|---|---|---|
| `interview_id` | Integer | FK to Interview (One-to-One) |
| `technical_score` | Integer | 1–5 |
| `communication_score` | Integer | 1–5 |
| `problem_solving_score` | Integer | 1–5 |
| `overall_score` | Float | Average of 3 scores |
| `recommendation` | String | Strongly Recommend / Recommend / Neutral / Do Not Recommend |
| `comments` | Text | Evaluator comments |

## API Endpoints

| Method | Endpoint | Roles | Description |
|---|---|---|---|
| GET | `/api/interviews` | All | List interviews (filtered by role) |
| GET | `/api/interviews/<id>` | All | Get single interview |
| POST | `/api/interviews` | Admin, HR, Recruiter | Schedule interview |
| PUT | `/api/interviews/<id>` | Admin, HR, Recruiter | Update interview |
| PATCH | `/api/interviews/<id>/status` | Admin, HR, Recruiter, Interviewer | Update status |
| DELETE | `/api/interviews/<id>` | Admin, HR, Recruiter | Delete interview |
| POST | `/api/interviews/<id>/feedback` | Admin, HR, Recruiter, Interviewer | Submit feedback |
| GET | `/api/interviews/<id>/feedback` | Admin, HR, Recruiter, Interviewer | Get feedback |
| PUT | `/api/interviews/<id>/feedback` | Admin, HR, Recruiter, Interviewer | Update feedback |

## Conflict Detection

When scheduling, the system checks for conflicts where the same interviewer is already booked at the same date and time. Cancelled interviews are excluded from conflict checks.

## Frontend Pages

| Route | File | Role |
|---|---|---|
| `/recruiter/interviews` | `RecruiterInterviews.jsx` | Recruiter |
| `/recruiter/interviews/schedule` | `InterviewForm.jsx` | Recruiter |
| `/recruiter/interviews/:id/feedback` | `InterviewFeedbackForm.jsx` | Recruiter |
| `/candidate/interviews` | `CandidateInterviews.jsx` | Candidate |
