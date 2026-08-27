# AI Candidate Ranking Module

## Overview

The Candidate Ranking module provides an AI-assisted, **transparent scoring system** to help recruiters prioritize candidates for open positions. It is a **decision-support tool only** — it does NOT automatically reject or hire candidates.

## Scoring Formula

| Factor | Weight | Description |
|---|---|---|
| Skill Match | 60% | Percentage of required skills found in candidate profile |
| Experience Match | 25% | Candidate's years of experience vs. job requirement |
| Education Match | 15% | Keyword match between candidate's education and job requirement |

### Final Score Calculation
```
Score = (skill_score × 0.60) + (exp_score × 0.25) + (edu_score × 0.15)
```

All scores range from 0–100. The final score is rounded to 2 decimal places.

## Fairness Policy

**Rankings NEVER use:**
- Gender, religion, caste, race, or ethnicity
- Age, disability, or medical history
- Marital status, political views, or financial information

Rankings use **only job-related fields**: required skills, experience years, and education requirements.

## API Endpoint

### Get Candidate Rankings for a Job
```
GET /api/jobs/<job_id>/rank-candidates
Authorization: Bearer <token>
Roles: Admin, HR, Recruiter
```

**Response:**
```json
{
  "success": true,
  "data": {
    "job_id": 1,
    "job_title": "Senior Python Engineer",
    "job_code": "JOB-0001",
    "candidates": [
      {
        "candidate_id": 5,
        "candidate_name": "Alex Kumar",
        "email": "alex@example.com",
        "score": 92.5,
        "skill_score": 100.0,
        "experience_score": 100.0,
        "education_score": 75.0,
        "experience_years": 6,
        "education": "B.Tech CS",
        "matched_skills": ["Python", "Flask", "SQL"],
        "missing_skills": ["Docker"],
        "application_status": "Shortlisted",
        "application_id": 12,
        "explanation": "Strong skill alignment. Meets or exceeds required experience."
      }
    ]
  }
}
```

### Shortlist a Candidate
```
PATCH /api/applications/<id>/shortlist
Authorization: Bearer <token>
Roles: Admin, HR, Recruiter
```

## Service: CandidateRanker

Location: `backend/app/services/candidate_ranker.py`

Key Methods:
- `rank_candidate_for_job(candidate, job)` — Returns a score dict for one candidate
- `rank_all_candidates_for_job(job_id)` — Returns sorted list of all candidates

## Frontend Page

**Route:** `/recruiter/rankings`
**File:** `frontend/src/pages/recruiter/RecruiterJobRankings.jsx`

Features:
- Job selection dropdown
- Run AI Ranking button
- Ranked table with progress bars, skill badges, explanations
- One-click Shortlist action
