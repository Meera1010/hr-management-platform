# Workforce Planning & Predictive Analytics

## Overview
The **Workforce Analytics Sub-System** provides annual headcount capacity forecasting, quarterly hiring targets per department, flight-risk attrition prediction scoring based on tenure and performance indicators, and salary competitiveness benchmarking against industry medians.

---

## Core Analytics Engine
- Headcount target vs actual gap calculation per department per quarter.
- Attrition risk scoring model evaluating tenure, performance ratings, and engagement metrics.
- Salary parity & market competitiveness index percentage calculation against industry median benchmarks.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/workforce/plans` | View annual workforce plans | `Admin`, `HR` |
| `GET` | `/api/workforce/attrition-risks` | View employee attrition risk scores | `Admin`, `HR` |
| `POST` | `/api/workforce/evaluate-attrition/<id>` | Re-evaluate attrition flight risk | `Admin`, `HR` |
| `GET` | `/api/workforce/benchmarks` | View market salary benchmarks | All Authenticated |
