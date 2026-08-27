from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.models.payroll import SalaryStructure, EmployeeSalary, PayrollRun, PaySlip, TaxDeclaration
from app.models.assets import AssetCategory, Asset, AssetAssignment, ITTicket, SoftwareLicense
from app.models.onboarding_exit import OnboardingChecklist, OnboardingTask, ResignationRequest, ExitClearance, FnFSettlement
from app.models.okr_performance import Objective, KeyResult, ReviewCycle, Feedback360, PerformanceImprovementPlan
from app.models.learning import Course, CourseModule, CourseEnrollment, Quiz, QuizQuestion, Certificate
from app.models.timesheet_shift import Timesheet, TimesheetEntry, Shift, EmployeeShiftRoster, OvertimeClaim
from app.models.expense_travel import ExpenseCategory, ExpenseClaim, ExpenseItem, TravelRequest
from app.models.compliance_audit import GrievanceTicket, CompanyPolicy, AuditLog
from app.models.workforce_analytics import WorkforcePlan, AttritionRiskScore, SalaryBenchmark
from datetime import datetime, date, timedelta

app = create_app()

def seed_enterprise_data():
    with app.app_context():
        print("Seeding enterprise sub-systems data...")

        # 1. Payroll & Compensation
        if not SalaryStructure.query.first():
            s1 = SalaryStructure(title="Standard Engineering Band", code="ENG-BAND-01", base_salary_pct=40.0, hra_pct=20.0, special_allowance_pct=20.0)
            s2 = SalaryStructure(title="Executive Leadership Band", code="EXEC-BAND-01", base_salary_pct=50.0, hra_pct=25.0, special_allowance_pct=15.0)
            db.session.add_all([s1, s2])
            db.session.commit()

        employees = Employee.query.all()
        for emp in employees:
            if not EmployeeSalary.query.filter_by(employee_id=emp.id).first():
                ctc = 1200000.0 if emp.designation == 'Senior Software Engineer' else 800000.0
                sal = EmployeeSalary(
                    employee_id=emp.id,
                    annual_ctc=ctc,
                    monthly_gross=ctc/12.0,
                    basic_pay=(ctc/12.0)*0.40,
                    hra=(ctc/12.0)*0.20,
                    special_allowance=(ctc/12.0)*0.20,
                    conveyance_allowance=1600.0,
                    medical_allowance=1250.0,
                    pf_deduction=1800.0,
                    professional_tax=200.0,
                    effective_date=date(2026, 1, 1)
                )
                db.session.add(sal)
        db.session.commit()

        # 2. Asset Categories & Assets
        if not AssetCategory.query.first():
            c1 = AssetCategory(name="Laptops & Workstations", code="CAT-LAPTOP", description="Apple silicon & Dell XPS Developer Edition laptops")
            c2 = AssetCategory(name="Monitors & Displays", code="CAT-MONITOR", description="4K Color accurate external displays")
            db.session.add_all([c1, c2])
            db.session.flush()

            a1 = Asset(asset_tag="AST-MAC-001", name="MacBook Pro 16 M3 Max", category_id=c1.id, serial_number="C02GX001M3", purchase_cost=249900.0, status="Assigned")
            a2 = Asset(asset_tag="AST-DELL-002", name="Dell XPS 15 9530", category_id=c1.id, serial_number="DELL9530X", purchase_cost=189900.0, status="Available")
            db.session.add_all([a1, a2])
            db.session.commit()

            if employees:
                assign = AssetAssignment(asset_id=a1.id, employee_id=employees[0].id, assigned_date=date(2026, 1, 15), status="Active")
                db.session.add(assign)
                db.session.commit()

        # 3. Onboarding & Exit
        if employees and not OnboardingChecklist.query.first():
            chk = OnboardingChecklist(employee_id=employees[0].id, title="Senior Engineer Onboarding Checklist", overall_status="In Progress")
            db.session.add(chk)
            db.session.flush()

            t1 = OnboardingTask(checklist_id=chk.id, task_name="Identity Verification & Tax Declaration", category="Documentation", is_completed=True)
            t2 = OnboardingTask(checklist_id=chk.id, task_name="MacBook Setup & SSH Key Deployment", category="IT Setup", is_completed=True)
            t3 = OnboardingTask(checklist_id=chk.id, task_name="Complete Mandatory Security & Privacy Training", category="Training", is_completed=False)
            db.session.add_all([t1, t2, t3])
            db.session.commit()

        # 4. OKRs & 360 Feedback
        if not Objective.query.first():
            obj = Objective(title="Accelerate Platform Microservices Modernization", level="Department", period_quarter="2026-Q2", start_date=date(2026, 4, 1), end_date=date(2026, 6, 30), progress_pct=65.0, status="On Track")
            db.session.add(obj)
            db.session.flush()

            kr1 = KeyResult(objective_id=obj.id, title="Migrate 8 core monolith endpoints to FastAPI microservices", target_value=8.0, current_value=6.0, unit="Endpoints")
            kr2 = KeyResult(objective_id=obj.id, title="Reduce average API response latency under 120ms", target_value=120.0, current_value=95.0, unit="ms")
            db.session.add_all([kr1, kr2])
            db.session.commit()

        # 5. Learning & LXP
        if not Course.query.first():
            crs1 = Course(title="Enterprise Python & Flask Architecture", code="PY-501", category="Technical", level="Intermediate", duration_hours=12.0, is_mandatory=True)
            crs2 = Course(title="Generative AI & Data Privacy Security", code="AI-601", category="Security", level="Advanced", duration_hours=8.0, is_mandatory=True)
            db.session.add_all([crs1, crs2])
            db.session.commit()

        # 6. Timesheets & Shifts
        if not Shift.query.first():
            sh1 = Shift(name="General Morning Shift", code="SH-GEN-01", start_time="09:00", end_time="18:00")
            sh2 = Shift(name="Night Operations Roster", code="SH-NIGHT-02", start_time="21:00", end_time="06:00", is_night_shift=True)
            db.session.add_all([sh1, sh2])
            db.session.commit()

        # 7. Expense Categories & Travel
        if not ExpenseCategory.query.first():
            ec1 = ExpenseCategory(name="Client Travel & Transit", code="EXP-TRAVEL", max_limit_per_claim=25000.0)
            ec2 = ExpenseCategory(name="Meals & Client Entertainment", code="EXP-MEALS", max_limit_per_claim=10000.0)
            db.session.add_all([ec1, ec2])
            db.session.commit()

        # 8. Compliance & Company Policies
        if not CompanyPolicy.query.first():
            pol1 = CompanyPolicy(title="Code of Workplace Professional Conduct & Ethics", code="POL-ETHICS-01", category="Code of Conduct", content="Employees shall conduct business affairs with absolute integrity, transparency, and adherence to data privacy.", version="2.0")
            pol2 = CompanyPolicy(title="Information Security & Clean Desk Policy", code="POL-SEC-02", category="IT & Data Security", content="All hardware devices must be password protected with disk encryption enabled.", version="1.5")
            db.session.add_all([pol1, pol2])
            db.session.commit()

        # 9. Workforce Planning & Salary Benchmarks
        if not SalaryBenchmark.query.first():
            bm1 = SalaryBenchmark(job_title="Senior Software Engineer", experience_level="Senior", industry_min_ctc=1200000.0, industry_median_ctc=1600000.0, industry_max_ctc=2400000.0, company_avg_ctc=1650000.0)
            bm2 = SalaryBenchmark(job_title="HR Manager", experience_level="Mid", industry_min_ctc=900000.0, industry_median_ctc=1200000.0, industry_max_ctc=1800000.0, company_avg_ctc=1250000.0)
            db.session.add_all([bm1, bm2])
            db.session.commit()

        print("Enterprise data seeding completed successfully!")

if __name__ == '__main__':
    seed_enterprise_data()
