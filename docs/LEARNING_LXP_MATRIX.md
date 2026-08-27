# Learning Experience Platform (LXP) & Skill Matrix

## Overview
The **Learning Experience Platform (LXP) Sub-System** provides interactive course catalog publishing, multi-module reading/video content, automated quiz grading, digital certificate generation with unique verification hashes, and departmental skill gap analytics.

---

## Core Features
- Course creation with duration, category, and level tags.
- Multiple-choice quiz assessment engine with custom passing threshold.
- Automatic certificate issuance upon successful quiz completion.
- Course enrollment tracking and progress completion percentages.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/learning/courses` | List published LXP courses | All Authenticated |
| `POST` | `/api/learning/courses` | Publish new LXP course | `Admin`, `HR` |
| `GET` | `/api/learning/enrollments` | View course enrollments | All Authenticated |
| `POST` | `/api/learning/enrollments` | Enroll in a course | All Authenticated |
| `POST` | `/api/learning/quizzes/<id>/submit` | Submit quiz answers for grading | All Authenticated |
| `GET` | `/api/learning/certificates` | View earned certificates | All Authenticated |
