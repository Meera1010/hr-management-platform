# Expense Claims & Travel Pre-Approvals

## Overview
The **Expense & Travel Sub-System** facilitates employee reimbursement claim submission, multi-tier manager and finance approval workflows, receipt image metadata attachment, multi-currency support, and corporate travel pre-approval requests.

---

## Core Features
- Expense categories with max limit thresholds per claim.
- Multi-item claim submission with receipt reference links.
- Travel pre-approval requests with destination, departure/return dates, estimated cost, and advance payout requests.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/expenses/categories` | List active expense categories | All Authenticated |
| `GET` | `/api/expenses/claims` | View expense reimbursement claims | All Authenticated |
| `POST` | `/api/expenses/claims` | Submit expense claim | All Authenticated |
| `GET` | `/api/expenses/travel-requests` | View business travel requests | All Authenticated |
| `POST` | `/api/expenses/travel-requests` | Submit business travel pre-approval | All Authenticated |
