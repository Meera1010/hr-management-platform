from datetime import datetime
from app import db

class SalaryStructure(db.Model):
    __tablename__ = 'salary_structures'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_salary_pct = db.Column(db.Float, default=40.0)  # % of CTC
    hra_pct = db.Column(db.Float, default=20.0)          # % of CTC
    special_allowance_pct = db.Column(db.Float, default=20.0)
    pf_employer_pct = db.Column(db.Float, default=12.0)
    pf_employee_pct = db.Column(db.Float, default=12.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee_salaries = db.relationship('EmployeeSalary', backref='salary_structure', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'description': self.description,
            'base_salary_pct': self.base_salary_pct,
            'hra_pct': self.hra_pct,
            'special_allowance_pct': self.special_allowance_pct,
            'pf_employer_pct': self.pf_employer_pct,
            'pf_employee_pct': self.pf_employee_pct,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class EmployeeSalary(db.Model):
    __tablename__ = 'employee_salaries'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, unique=True)
    structure_id = db.Column(db.Integer, db.ForeignKey('salary_structures.id'), nullable=True)
    annual_ctc = db.Column(db.Float, nullable=False)
    monthly_gross = db.Column(db.Float, nullable=False)
    basic_pay = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, nullable=False)
    special_allowance = db.Column(db.Float, default=0.0)
    conveyance_allowance = db.Column(db.Float, default=0.0)
    medical_allowance = db.Column(db.Float, default=0.0)
    pf_deduction = db.Column(db.Float, default=0.0)
    esi_deduction = db.Column(db.Float, default=0.0)
    professional_tax = db.Column(db.Float, default=200.0)
    tds_deduction = db.Column(db.Float, default=0.0)
    bank_name = db.Column(db.String(100), nullable=True)
    bank_account_no = db.Column(db.String(50), nullable=True)
    ifsc_code = db.Column(db.String(20), nullable=True)
    pan_number = db.Column(db.String(20), nullable=True)
    effective_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('salary', uselist=False))
    payslips = db.relationship('PaySlip', backref='employee_salary', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'structure_id': self.structure_id,
            'structure_title': self.salary_structure.title if self.salary_structure else None,
            'annual_ctc': self.annual_ctc,
            'monthly_gross': self.monthly_gross,
            'basic_pay': self.basic_pay,
            'hra': self.hra,
            'special_allowance': self.special_allowance,
            'conveyance_allowance': self.conveyance_allowance,
            'medical_allowance': self.medical_allowance,
            'pf_deduction': self.pf_deduction,
            'esi_deduction': self.esi_deduction,
            'professional_tax': self.professional_tax,
            'tds_deduction': self.tds_deduction,
            'bank_name': self.bank_name,
            'bank_account_no': self.bank_account_no,
            'ifsc_code': self.ifsc_code,
            'pan_number': self.pan_number,
            'effective_date': self.effective_date.strftime('%Y-%m-%d') if self.effective_date else None,
            'is_active': self.is_active
        }


class PayrollRun(db.Model):
    __tablename__ = 'payroll_runs'

    id = db.Column(db.Integer, primary_key=True)
    pay_period_month = db.Column(db.Integer, nullable=False)  # 1 - 12
    pay_period_year = db.Column(db.Integer, nullable=False)   # e.g., 2026
    total_employees = db.Column(db.Integer, default=0)
    total_gross_payout = db.Column(db.Float, default=0.0)
    total_deductions = db.Column(db.Float, default=0.0)
    total_net_payout = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Draft')  # Draft, Processing, Approved, Paid, Cancelled
    processed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payslips = db.relationship('PaySlip', backref='payroll_run', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'pay_period_month': self.pay_period_month,
            'pay_period_year': self.pay_period_year,
            'period_label': f"{self.pay_period_year}-{self.pay_period_month:02d}",
            'total_employees': self.total_employees,
            'total_gross_payout': self.total_gross_payout,
            'total_deductions': self.total_deductions,
            'total_net_payout': self.total_net_payout,
            'status': self.status,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PaySlip(db.Model):
    __tablename__ = 'payslips'

    id = db.Column(db.Integer, primary_key=True)
    payroll_run_id = db.Column(db.Integer, db.ForeignKey('payroll_runs.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee_salary_id = db.Column(db.Integer, db.ForeignKey('employee_salaries.id'), nullable=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    working_days = db.Column(db.Integer, default=30)
    payable_days = db.Column(db.Float, default=30.0)
    basic_pay = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, nullable=False)
    special_allowance = db.Column(db.Float, default=0.0)
    conveyance_allowance = db.Column(db.Float, default=0.0)
    medical_allowance = db.Column(db.Float, default=0.0)
    bonus_payout = db.Column(db.Float, default=0.0)
    overtime_payout = db.Column(db.Float, default=0.0)
    gross_earnings = db.Column(db.Float, nullable=False)
    pf_deduction = db.Column(db.Float, default=0.0)
    esi_deduction = db.Column(db.Float, default=0.0)
    professional_tax = db.Column(db.Float, default=0.0)
    tds_deduction = db.Column(db.Float, default=0.0)
    unpaid_leave_deduction = db.Column(db.Float, default=0.0)
    other_deductions = db.Column(db.Float, default=0.0)
    total_deductions = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(30), default='Pending')  # Pending, Processing, Paid
    payment_mode = db.Column(db.String(30), default='Direct Deposit')
    transaction_reference = db.Column(db.String(100), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='payslips', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'payroll_run_id': self.payroll_run_id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'employee_code': self.employee.employee_code if self.employee else None,
            'department': self.employee.department.name if self.employee and self.employee.department else None,
            'month': self.month,
            'year': self.year,
            'period_label': f"{self.year}-{self.month:02d}",
            'working_days': self.working_days,
            'payable_days': self.payable_days,
            'basic_pay': self.basic_pay,
            'hra': self.hra,
            'special_allowance': self.special_allowance,
            'conveyance_allowance': self.conveyance_allowance,
            'medical_allowance': self.medical_allowance,
            'bonus_payout': self.bonus_payout,
            'overtime_payout': self.overtime_payout,
            'gross_earnings': self.gross_earnings,
            'pf_deduction': self.pf_deduction,
            'esi_deduction': self.esi_deduction,
            'professional_tax': self.professional_tax,
            'tds_deduction': self.tds_deduction,
            'unpaid_leave_deduction': self.unpaid_leave_deduction,
            'other_deductions': self.other_deductions,
            'total_deductions': self.total_deductions,
            'net_salary': self.net_salary,
            'payment_status': self.payment_status,
            'payment_mode': self.payment_mode,
            'transaction_reference': self.transaction_reference,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None
        }


class TaxDeclaration(db.Model):
    __tablename__ = 'tax_declarations'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    financial_year = db.Column(db.String(20), nullable=False)  # e.g., "2026-2027"
    regime = db.Column(db.String(20), default='New')            # Old, New
    sec_80c_ppf_elss = db.Column(db.Float, default=0.0)
    sec_80d_health_insurance = db.Column(db.Float, default=0.0)
    hra_rent_paid_annual = db.Column(db.Float, default=0.0)
    home_loan_interest_sec24 = db.Column(db.Float, default=0.0)
    other_exemptions = db.Column(db.Float, default=0.0)
    total_declared_investments = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Submitted')     # Draft, Submitted, Verified, Rejected
    verified_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('Employee', backref='tax_declarations', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'financial_year': self.financial_year,
            'regime': self.regime,
            'sec_80c_ppf_elss': self.sec_80c_ppf_elss,
            'sec_80d_health_insurance': self.sec_80d_health_insurance,
            'hra_rent_paid_annual': self.hra_rent_paid_annual,
            'home_loan_interest_sec24': self.home_loan_interest_sec24,
            'other_exemptions': self.other_exemptions,
            'total_declared_investments': self.total_declared_investments,
            'status': self.status,
            'comments': self.comments,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
