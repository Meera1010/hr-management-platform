# Data Privacy and Security Policy

## ⚠️ Important Warning
This project is an **educational demonstration** of an AI-Powered HR Platform. 

**DO NOT USE REAL PERSONAL DATA.**

### Core Data Policies:
1. **Synthetic Data Only**: All users, candidates, employees, and resumes entered into this system must be entirely fictional.
2. **No Real Employee Data**: Do not upload real organization structure, performance reviews, or personal details.
3. **Prohibited Information**: Under no circumstances should the system store:
    * Government identification numbers (Aadhaar, PAN, SSN, Passport, etc.)
    * Bank account or credit/debit card information
    * Health or medical records
    * Biometric information
    * Real passwords or security keys
    * Real personal addresses, phone numbers, or email addresses

### Security Architecture
* **Authentication**: Secured via JWT (JSON Web Tokens).
* **Passwords**: Passwords are securely hashed using Werkzeug (`pbkdf2:sha256`); plaintext passwords are never stored.
* **Secrets Management**: Configuration and secret keys (e.g., `JWT_SECRET_KEY`) are stored in environment variables, never committed to source control.
* **Role-Based Access Control**: Strict decorators (`@admin_required`, `@hr_required`) restrict API routes to authorized roles only.

By using this system, you acknowledge that it is a demo environment and agree to populate it solely with fictional demo information.
