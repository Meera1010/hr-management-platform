# OKRs & 360-Degree Performance Management

## Overview
The **OKR & 360 Performance Sub-System** tracks Objectives & Key Results (OKRs) across Company, Department, Team, and Individual levels, facilitates multi-rater 360-degree feedback reviews, competency matrix evaluations, and Performance Improvement Plans (PIPs).

---

## Key Features

### 1. OKR Cascading & Progress Calculation
- Objectives categorized by level, quarter, and owner.
- Weighted key results with target vs current numerical values.
- Automatic progress aggregation (`Completed`, `On Track`, `At Risk`, `Behind`).

### 2. 360-Degree Multi-Rater Feedback
- Feedback evaluations across `Self`, `Peer`, `Manager`, and `Direct Report` relationships.
- Multi-metric ratings (Leadership, Technical, Communication, Teamwork, Overall Score out of 5.0).
- Qualitative feedback sections for strengths and areas for improvement.

### 3. Performance Improvement Plans (PIPs)
- Formal PIP tracking for underperforming employees with explicit target milestones, support resources, and final outcome evaluation.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/okrs/objectives` | List OKRs with filters | All Authenticated |
| `POST` | `/api/okrs/objectives` | Create new OKR objective | All Authenticated |
| `POST` | `/api/okrs/objectives/<id>/key-results` | Add key result to objective | All Authenticated |
| `POST` | `/api/okrs/key-results/<id>/update-progress` | Update key result current value | All Authenticated |
| `GET` | `/api/okrs/review-cycles` | List active 360 review cycles | All Authenticated |
| `GET` | `/api/okrs/360-feedback` | View assigned 360 feedback forms | All Authenticated |
| `GET` | `/api/okrs/pips` | View PIP tracking records | All Authenticated |
