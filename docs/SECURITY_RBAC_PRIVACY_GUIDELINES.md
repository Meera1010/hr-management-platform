# Security, RBAC & Privacy Compliance Guidelines

## Overview
This document specifies the Data Security Architecture, RBAC Policy Controls, Encryption Standards, Privacy Compliance Protocols, and Safe Demo Data Handling for the **AI-Powered HR, Recruitment & Employee Management Platform**.

---

## 1. Authentication & Encryption Architecture

### Password Hashing Standards
- All user passwords are encrypted using **Werkzeug's PBKDF2 with SHA-256** key derivation with dynamic salt generation.
- Raw plain-text passwords are never stored in database columns or application memory logs.

### JWT Session Token Security
- Session authentication utilizes **JSON Web Tokens (JWT)** with HMAC-SHA256 signatures.
- Access tokens expire after 24 hours.
- Token validation decorators enforce signature authenticity, expiration timelines, and non-empty sub identities before granting endpoint access.

---

## 2. Privacy & Zero-PFI/PII Demo Data Policy

### Fictional Demo Data Enforcement
- **100% Synthetic Data**: All employee names, email addresses, mobile numbers, company names, salary amounts, and bank account numbers are entirely synthetic demo records.
- **Zero Real Identifiers**: No real government identity numbers (Aadhaar, PAN, SSN), actual bank account numbers, or real medical records are ever stored or processed by the system.
- **AI Decision Support**: AI scoring engines (Resume Match %, Flight Risk Scores, Candidate Rankings) serve strictly as non-discriminatory decision-support recommendations for human recruiters and HR managers. Final hiring, promotion, and termination decisions require human sign-off.

---

## 3. Security Audit Logging & Compliance Controls
- Every sensitive mutation (salary modification, role changes, resignation approvals, policy edits) is logged to the immutable `audit_logs` table.
- Log entries capture:
  - Performing User ID & Email
  - Action Identifier (`CREATE`, `UPDATE`, `DELETE`, `APPROVE`)
  - Target Entity Type & Entity ID
  - JSON serialization of field-level deltas (`old_value` vs `new_value`)
  - Client IP Address & UTC Timestamp
