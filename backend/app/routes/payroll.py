from flask import Blueprint, request, jsonify
from app import db
from app.models.payroll import SalaryStructure, EmployeeSalary, PayrollRun, PaySlip, TaxDeclaration
from app.services.payroll_service import PayrollService
from app.utils.auth import token_required, role_required
from datetime import datetime, date

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/structures', methods=['GET'])
@token_required
def get_structures(current_user):
    structures = SalaryStructure.query.all()
    return jsonify({'structures': [s.to_dict() for s in structures]}), 200

@payroll_bp.route('/structures', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def create_structure(current_user):
    data = request.get_json() or {}
    if not data.get('title') or not data.get('code'):
        return jsonify({'message': 'Title and Code are required'}), 400

    structure = SalaryStructure(
        title=data['title'],
        code=data['code'],
        description=data.get('description'),
        base_salary_pct=data.get('base_salary_pct', 40.0),
        hra_pct=data.get('hra_pct', 20.0),
        special_allowance_pct=data.get('special_allowance_pct', 20.0),
        pf_employer_pct=data.get('pf_employer_pct', 12.0),
        pf_employee_pct=data.get('pf_employee_pct', 12.0)
    )
    db.session.add(structure)
    db.session.commit()
    return jsonify({'message': 'Salary structure created', 'structure': structure.to_dict()}), 201

@payroll_bp.route('/employee-salaries', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_employee_salaries(current_user):
    salaries = EmployeeSalary.query.all()
    return jsonify({'salaries': [s.to_dict() for s in salaries]}), 200

@payroll_bp.route('/employee-salaries', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def set_employee_salary(current_user):
    data = request.get_json() or {}
    employee_id = data.get('employee_id')
    annual_ctc = data.get('annual_ctc')

    if not employee_id or not annual_ctc:
        return jsonify({'message': 'employee_id and annual_ctc are required'}), 400

    calc = PayrollService.calculate_salary_breakdown(float(annual_ctc))

    emp_sal = EmployeeSalary.query.filter_by(employee_id=employee_id).first()
    if not emp_sal:
        emp_sal = EmployeeSalary(
            employee_id=employee_id,
            structure_id=data.get('structure_id'),
            annual_ctc=float(annual_ctc),
            monthly_gross=calc['monthly_gross'],
            basic_pay=calc['basic_pay'],
            hra=calc['hra'],
            special_allowance=calc['special_allowance'],
            conveyance_allowance=calc['conveyance_allowance'],
            medical_allowance=calc['medical_allowance'],
            pf_deduction=calc['pf_deduction'],
            esi_deduction=calc['esi_deduction'],
            professional_tax=calc['professional_tax'],
            tds_deduction=calc['tds_deduction'],
            bank_name=data.get('bank_name', 'HDFC Bank'),
            bank_account_no=data.get('bank_account_no', '501002349012'),
            ifsc_code=data.get('ifsc_code', 'HDFC0000123'),
            pan_number=data.get('pan_number', 'ABCDE1234F'),
            effective_date=datetime.strptime(data.get('effective_date', date.today().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        )
        db.session.add(emp_sal)
    else:
        emp_sal.annual_ctc = float(annual_ctc)
        emp_sal.monthly_gross = calc['monthly_gross']
        emp_sal.basic_pay = calc['basic_pay']
        emp_sal.hra = calc['hra']
        emp_sal.special_allowance = calc['special_allowance']
        emp_sal.conveyance_allowance = calc['conveyance_allowance']
        emp_sal.medical_allowance = calc['medical_allowance']
        emp_sal.pf_deduction = calc['pf_deduction']
        emp_sal.esi_deduction = calc['esi_deduction']
        emp_sal.professional_tax = calc['professional_tax']
        emp_sal.tds_deduction = calc['tds_deduction']
        if data.get('bank_name'): emp_sal.bank_name = data['bank_name']
        if data.get('bank_account_no'): emp_sal.bank_account_no = data['bank_account_no']

    db.session.commit()
    return jsonify({'message': 'Employee salary configured successfully', 'salary': emp_sal.to_dict()}), 200

@payroll_bp.route('/runs', methods=['GET'])
@token_required
@role_required(['Admin', 'HR'])
def get_payroll_runs(current_user):
    runs = PayrollRun.query.order_by(PayrollRun.pay_period_year.desc(), PayrollRun.pay_period_month.desc()).all()
    return jsonify({'runs': [r.to_dict() for r in runs]}), 200

@payroll_bp.route('/runs/execute', methods=['POST'])
@token_required
@role_required(['Admin', 'HR'])
def execute_payroll_run(current_user):
    data = request.get_json() or {}
    month = data.get('month', date.today().month)
    year = data.get('year', date.today().year)

    try:
        run = PayrollService.run_payroll_for_month(int(month), int(year), current_user.id)
        return jsonify({'message': f'Payroll run for {year}-{month:02d} completed', 'run': run.to_dict()}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@payroll_bp.route('/payslips', methods=['GET'])
@token_required
def get_payslips(current_user):
    if current_user.role in ['Admin', 'HR']:
        employee_id = request.args.get('employee_id')
        if employee_id:
            payslips = PaySlip.query.filter_by(employee_id=employee_id).all()
        else:
            payslips = PaySlip.query.all()
    else:
        emp = getattr(current_user, 'employee', None)
        if not emp:
            return jsonify({'payslips': []}), 200
        payslips = PaySlip.query.filter_by(employee_id=emp.id).all()

    return jsonify({'payslips': [p.to_dict() for p in payslips]}), 200

@payroll_bp.route('/tax-declarations', methods=['GET'])
@token_required
def get_tax_declarations(current_user):
    if current_user.role in ['Admin', 'HR']:
        declarations = TaxDeclaration.query.all()
    else:
        emp = getattr(current_user, 'employee', None) or getattr(current_user, 'employee_profile', None)
        if not emp:
            return jsonify({'declarations': []}), 200
        declarations = TaxDeclaration.query.filter_by(employee_id=emp.id).all()

    return jsonify({'declarations': [d.to_dict() for d in declarations]}), 200

@payroll_bp.route('/tax-declarations', methods=['POST'])
@token_required
def submit_tax_declaration(current_user):
    data = request.get_json() or {}
    emp = getattr(current_user, 'employee', None) or getattr(current_user, 'employee_profile', None)
    if current_user.role in ['Admin', 'HR'] and data.get('employee_id'):
        emp_id = data['employee_id']
    else:
        emp_id = emp.id if emp else current_user.id

    financial_year = data.get('financial_year', '2026-2027')
    declaration = TaxDeclaration.query.filter_by(employee_id=emp_id, financial_year=financial_year).first()

    sec_80c = float(data.get('sec_80c_ppf_elss', 0.0))
    sec_80d = float(data.get('sec_80d_health_insurance', 0.0))
    hra_rent = float(data.get('hra_rent_paid_annual', 0.0))
    home_loan = float(data.get('home_loan_interest_sec24', 0.0))
    other_ex = float(data.get('other_exemptions', 0.0))
    total_declared = sec_80c + sec_80d + hra_rent + home_loan + other_ex

    if not declaration:
        declaration = TaxDeclaration(
            employee_id=emp_id,
            financial_year=financial_year,
            regime=data.get('regime', 'New'),
            sec_80c_ppf_elss=sec_80c,
            sec_80d_health_insurance=sec_80d,
            hra_rent_paid_annual=hra_rent,
            home_loan_interest_sec24=home_loan,
            other_exemptions=other_ex,
            total_declared_investments=total_declared,
            status='Submitted'
        )
        db.session.add(declaration)
    else:
        declaration.regime = data.get('regime', declaration.regime)
        declaration.sec_80c_ppf_elss = sec_80c
        declaration.sec_80d_health_insurance = sec_80d
        declaration.hra_rent_paid_annual = hra_rent
        declaration.home_loan_interest_sec24 = home_loan
        declaration.other_exemptions = other_ex
        declaration.total_declared_investments = total_declared
        declaration.status = 'Submitted'

    db.session.commit()
    return jsonify({'message': 'Tax declaration submitted', 'declaration': declaration.to_dict()}), 201
