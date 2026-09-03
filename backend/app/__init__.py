import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config, DB_DIR
from dotenv import load_dotenv

# Load env variables
load_dotenv()

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    cors_origins = [o.strip() for o in os.environ.get('CORS_ORIGINS', '').split(',') if o.strip()]
    CORS(app, resources={r"/api/*": {"origins": cors_origins}} if cors_origins else {})
    
    jwt = JWTManager(app)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401
        
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401
        
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401

    # Root landing route
    @app.route('/', methods=['GET'])
    def root_landing():
        return """
        <!DOCTYPE html>
        <html>
        <head><title>AI HR Platform API</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
          <h1 style="color: #4f46e5;">AI HR Platform Backend API Server</h1>
          <p style="font-size: 1.2rem;">The REST API backend is active on <strong>http://localhost:5000/api</strong></p>
          <div style="margin-top: 20px; padding: 20px; background: #f3f4f6; border-radius: 8px; display: inline-block;">
            <p style="margin-bottom: 15px; font-weight: 500;">To use the Interactive Web Interface, open:</p>
            <a href="http://localhost:5173" style="display: inline-block; background: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Open Web App (http://localhost:5173)</a>
          </div>
        </body>
        </html>
        """

    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "success",
            "message": "AI HR Platform API is running"
        })


    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.roles import roles_bp
    from app.routes.auth import auth_bp
    from app.routes.departments import departments_bp
    from app.routes.employees import employees_bp
    from .routes.jobs import jobs_bp
    from .routes.candidates import candidates_bp
    from .routes.applications import applications_bp
    from .routes.resumes import resumes_bp
    from .routes.matching import matching_bp
    from .routes.ranking import ranking_bp
    from .routes.interviews import interviews_bp
    from .routes.offers import offers_bp
    from .routes.attendance import attendance_bp
    from .routes.leaves import leaves_bp
    from .routes.performance import performance_bp
    from .routes.training import training_bp
    from .routes.notifications import notifications_bp
    from .routes.dashboards import dashboards_bp
    from .routes.analytics import analytics_bp
    from .routes.reports import reports_bp
    from .routes.search import search_bp
    from .routes.recommendations import recommendations_bp
    from .routes.payroll import payroll_bp
    from .routes.assets import assets_bp
    from .routes.onboarding_exit import onboarding_exit_bp
    from .routes.okrs import okrs_bp
    from .routes.learning import learning_bp
    from .routes.timesheets import timesheets_bp
    from .routes.expenses import expenses_bp
    from .routes.compliance import compliance_bp
    from .routes.workforce import workforce_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(departments_bp, url_prefix='/api/departments')
    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(candidates_bp, url_prefix='/api/candidates')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(resumes_bp, url_prefix='/api/resumes')
    app.register_blueprint(matching_bp, url_prefix='/api')
    app.register_blueprint(ranking_bp, url_prefix='/api')
    app.register_blueprint(interviews_bp, url_prefix='/api/interviews')
    app.register_blueprint(offers_bp, url_prefix='/api/offers')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(leaves_bp, url_prefix='/api/leaves')
    app.register_blueprint(performance_bp, url_prefix='/api/performance')
    app.register_blueprint(training_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(payroll_bp, url_prefix='/api/payroll')
    app.register_blueprint(assets_bp, url_prefix='/api/assets')
    app.register_blueprint(onboarding_exit_bp, url_prefix='/api/lifecycle')
    app.register_blueprint(okrs_bp, url_prefix='/api/okrs')
    app.register_blueprint(learning_bp, url_prefix='/api/learning')
    app.register_blueprint(timesheets_bp, url_prefix='/api/timesheets')
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    app.register_blueprint(compliance_bp, url_prefix='/api/compliance')
    app.register_blueprint(workforce_bp, url_prefix='/api/workforce')


    # Create db tables on startup if they don't exist
    with app.app_context():
        # Import models so SQLAlchemy knows about them before creating tables
        from app.models.role import Role
        from app.models.user import User
        from app.models.department import Department
        from app.models.employee import Employee
        from app.models.job import Job
        from app.models.candidate import Candidate
        from app.models.application import Application
        from app.models.resume import Resume
        from app.models.skill import Skill
        from app.models.interview import Interview
        from app.models.interview_feedback import InterviewFeedback
        from app.models.offer import Offer
        from app.models.attendance import Attendance
        from app.models.leave_request import LeaveRequest
        from app.models.performance_review import PerformanceReview
        from app.models.training import TrainingCourse, TrainingAssignment
        from app.models.notification import Notification
        from app.models.payroll import SalaryStructure, EmployeeSalary, PayrollRun, PaySlip, TaxDeclaration
        from app.models.assets import AssetCategory, Asset, AssetAssignment, AssetMaintenance, SoftwareLicense, ITTicket
        from app.models.onboarding_exit import OnboardingChecklist, OnboardingTask, EmployeeDocument, ResignationRequest, ExitClearance, FnFSettlement
        from app.models.okr_performance import Objective, KeyResult, ReviewCycle, Feedback360, PerformanceImprovementPlan
        from app.models.learning import Course, CourseModule, CourseEnrollment, Quiz, QuizQuestion, Certificate
        from app.models.timesheet_shift import Timesheet, TimesheetEntry, Shift, EmployeeShiftRoster, OvertimeClaim
        from app.models.expense_travel import ExpenseCategory, ExpenseClaim, ExpenseItem, TravelRequest
        from app.models.compliance_audit import GrievanceTicket, GrievanceLog, CompanyPolicy, PolicyAcknowledgment, AuditLog
        from app.models.workforce_analytics import WorkforcePlan, AttritionRiskScore, SalaryBenchmark
        db.create_all()

    return app
