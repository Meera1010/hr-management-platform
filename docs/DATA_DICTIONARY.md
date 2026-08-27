# Enterprise Data Dictionary & Entity Definitions

## Overview
This document contains the complete technical data dictionary for all entity tables, field names, data types, constraints, default values, foreign key relationships, and index definitions in the **AI HR Platform**.

---

## 1. Core Authentication Entities

### Table: `users`
| Field | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto Increment | Unique user identifier |
| `first_name` | String(50) | Not Null | User first name |
| `last_name` | String(50) | Not Null | User last name |
| `email` | String(120) | Unique, Not Null, Index | User email address |
| `phone` | String(20) | Nullable | Contact phone number |
| `password_hash` | String(255) | Not Null | Werkzeug generate_password_hash |
| `role_id` | Integer | FK -> `roles.id`, Not Null | Associated system role |
| `is_active` | Boolean | Default True | Account activation state |
| `created_at` | DateTime | Default UTC | Account creation timestamp |

---

## 2. Payroll & Compensation Entities

### Table: `salary_structures`
| Field | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique structure ID |
| `title` | String(100) | Not Null | Structure title band |
| `code` | String(30) | Unique, Not Null | Structure code |
| `base_salary_pct` | Float | Default 40.0 | % of CTC allocated to Basic Pay |
| `hra_pct` | Float | Default 20.0 | % of CTC allocated to HRA |
| `special_allowance_pct` | Float | Default 20.0 | % of CTC allocated to Special Allowance |
| `pf_employer_pct` | Float | Default 12.0 | Employer PF contribution rate |
| `pf_employee_pct` | Float | Default 12.0 | Employee PF deduction rate |

### Table: `employee_salaries`
| Field | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Salary record ID |
| `employee_id` | Integer | FK -> `employees.id`, Unique | Associated employee |
| `annual_ctc` | Float | Not Null | Cost to Company (CTC) |
| `monthly_gross` | Float | Not Null | Monthly gross earnings |
| `basic_pay` | Float | Not Null | Basic pay component |
| `hra` | Float | Not Null | House rent allowance component |
| `pf_deduction` | Float | Default 0.0 | Monthly PF deduction |
| `professional_tax` | Float | Default 200.0 | Monthly PT deduction |
| `bank_account_no` | String(50) | Nullable | Direct deposit bank account |
| `ifsc_code` | String(20) | Nullable | Bank IFSC routing code |

---

## 3. IT Asset Management Entities

### Table: `assets`
| Field | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique asset ID |
| `asset_tag` | String(50) | Unique, Not Null | Unique barcode/tag identifier |
| `name` | String(150) | Not Null | Asset hardware name |
| `category_id` | Integer | FK -> `asset_categories.id` | Hardware category |
| `serial_number` | String(100) | Unique, Nullable | Manufacturer serial number |
| `purchase_cost` | Float | Default 0.0 | Purchase acquisition cost |
| `status` | String(30) | Default 'Available' | Available, Assigned, Maintenance |
