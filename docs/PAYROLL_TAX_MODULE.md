# Payroll, Compensation & Tax Management Module

## Overview
The **Payroll & Compensation Management Sub-System** provides end-to-end salary structure configuration, automated tax deduction calculations, monthly payroll processing, payslip PDF/data generation, annual tax declaration worksheets, and bank payout batch exports.

---

## Data Privacy & Safety Compliance
> All monetary numbers, bank account numbers, IFSC codes, PAN identifiers, and employee records in this module are **100% fictional/demo data**. No real financial accounts, tax filings, or personal banking information are stored or processed.

---

## Core Features & Workflows

### 1. Salary Structure Configuration
- Configurable base salary percentage (e.g. 40% of CTC).
- House Rent Allowance (HRA), Special Allowance, Conveyance, and Medical Allowance rules.
- Employer & Employee Provident Fund (PF) contribution ceilings.

### 2. Tax Slab & Deductions Engine
- Automated income tax (TDS) estimation for New and Old Tax Regimes.
- Standard Professional Tax (PT) calculations.
- ESI (Employee State Insurance) deduction applicability thresholds.

### 3. Monthly Payroll Processing Run
- One-click batch payroll execution per pay period.
- Validation against working days and unpaid leave deductions.
- State transitions: `Draft` -> `Processing` -> `Approved` -> `Paid`.

### 4. Employee Tax Declarations
- Annual investment declaration worksheets under Section 80C, 80D, HRA rent receipts, Home Loan interest Section 24.
- HR verification and proof document audit workflows.

---

## API Endpoints Reference

| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/payroll/structures` | List all configured salary structures | `Admin`, `HR`, `Employee` |
| `POST` | `/api/payroll/structures` | Create a new salary structure band | `Admin`, `HR` |
| `GET` | `/api/payroll/employee-salaries` | Retrieve employee compensation details | `Admin`, `HR` |
| `POST` | `/api/payroll/employee-salaries` | Configure annual CTC & bank account info | `Admin`, `HR` |
| `GET` | `/api/payroll/runs` | Get history of monthly payroll runs | `Admin`, `HR` |
| `POST` | `/api/payroll/runs/execute` | Execute monthly payroll calculation run | `Admin`, `HR` |
| `GET` | `/api/payroll/payslips` | Download & view employee payslips | `Admin`, `HR`, `Employee` |
| `GET` | `/api/payroll/tax-declarations` | View annual tax declaration worksheets | `Admin`, `HR`, `Employee` |
| `POST` | `/api/payroll/tax-declarations` | Submit investment declaration proof | `Admin`, `HR`, `Employee` |

---

## Database Models Architecture
- `SalaryStructure`: Template for base, HRA, allowance, and PF percentages.
- `EmployeeSalary`: Individual employee CTC, gross, deductions, and bank details.
- `PayrollRun`: Batch run header summarizing total headcount, gross, deductions, and net payout.
- `PaySlip`: Line-item breakdown per employee per month.
- `TaxDeclaration`: Investment declarations under Sec 80C, 80D, HRA, Home Loan.
