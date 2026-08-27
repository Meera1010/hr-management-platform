from app import db
from app.models.payroll import SalaryStructure, EmployeeSalary, PayrollRun, PaySlip, TaxDeclaration
from datetime import datetime, date

class PayrollService:
    @staticmethod
    def calculate_salary_breakdown(annual_ctc):
        """Calculates monthly components based on standard enterprise rules."""
        monthly_gross = round(annual_ctc / 12.0, 2)
        basic_pay = round(monthly_gross * 0.40, 2)
        hra = round(monthly_gross * 0.20, 2)
        conveyance = 1600.0
        medical = 1250.0
        special_allowance = round(max(0, monthly_gross - (basic_pay + hra + conveyance + medical)), 2)

        # Standard PF & PT
        pf_deduction = round(min(basic_pay * 0.12, 1800.0), 2)
        esi_deduction = round(monthly_gross * 0.0075, 2) if monthly_gross <= 21000.0 else 0.0
        professional_tax = 200.0

        # Estimated TDS tax slab calculation (New Tax Regime approx)
        tds_deduction = 0.0
        if annual_ctc > 1200000:
            tds_deduction = round((annual_ctc * 0.12) / 12.0, 2)
        elif annual_ctc > 700000:
            tds_deduction = round((annual_ctc * 0.05) / 12.0, 2)

        total_deductions = round(pf_deduction + esi_deduction + professional_tax + tds_deduction, 2)
        net_salary = round(monthly_gross - total_deductions, 2)

        return {
            'annual_ctc': annual_ctc,
            'monthly_gross': monthly_gross,
            'basic_pay': basic_pay,
            'hra': hra,
            'special_allowance': special_allowance,
            'conveyance_allowance': conveyance,
            'medical_allowance': medical,
            'pf_deduction': pf_deduction,
            'esi_deduction': esi_deduction,
            'professional_tax': professional_tax,
            'tds_deduction': tds_deduction,
            'total_deductions': total_deductions,
            'net_salary': net_salary
        }

    @staticmethod
    def run_payroll_for_month(month, year, processed_by_id):
        """Generates payslips for all active employees for the given month."""
        existing_run = PayrollRun.query.filter_by(pay_period_month=month, pay_period_year=year).first()
        if existing_run and existing_run.status in ['Approved', 'Paid']:
            raise ValueError(f"Payroll for {year}-{month:02d} is already finalized.")

        if not existing_run:
            payroll_run = PayrollRun(
                pay_period_month=month,
                pay_period_year=year,
                status='Processing',
                processed_by_id=processed_by_id,
                processed_at=datetime.utcnow()
            )
            db.session.add(payroll_run)
            db.session.flush()
        else:
            payroll_run = existing_run
            payroll_run.status = 'Processing'
            # Delete draft payslips to re-compute
            PaySlip.query.filter_by(payroll_run_id=payroll_run.id).delete()

        salaries = EmployeeSalary.query.filter_by(is_active=True).all()
        total_gross = 0.0
        total_ded = 0.0

        for sal in salaries:
            breakdown = PayrollService.calculate_salary_breakdown(sal.annual_ctc)
            payslip = PaySlip(
                payroll_run_id=payroll_run.id,
                employee_id=sal.employee_id,
                employee_salary_id=sal.id,
                month=month,
                year=year,
                working_days=30,
                payable_days=30.0,
                basic_pay=breakdown['basic_pay'],
                hra=breakdown['hra'],
                special_allowance=breakdown['special_allowance'],
                conveyance_allowance=breakdown['conveyance_allowance'],
                medical_allowance=breakdown['medical_allowance'],
                gross_earnings=breakdown['monthly_gross'],
                pf_deduction=breakdown['pf_deduction'],
                esi_deduction=breakdown['esi_deduction'],
                professional_tax=breakdown['professional_tax'],
                tds_deduction=breakdown['tds_deduction'],
                total_deductions=breakdown['total_deductions'],
                net_salary=breakdown['net_salary'],
                payment_status='Pending'
            )
            db.session.add(payslip)
            total_gross += breakdown['monthly_gross']
            total_ded += breakdown['total_deductions']

        payroll_run.total_employees = len(salaries)
        payroll_run.total_gross_payout = round(total_gross, 2)
        payroll_run.total_deductions = round(total_ded, 2)
        payroll_run.total_net_payout = round(total_gross - total_ded, 2)
        payroll_run.status = 'Approved'
        payroll_run.approved_at = datetime.utcnow()

        db.session.commit()
        return payroll_run
