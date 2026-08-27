from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
from dotenv import load_dotenv

# Load env variables
load_dotenv()

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
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
    from app.routes.jobs import jobs_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(departments_bp, url_prefix='/api/departments')
    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')

    # Create db tables on startup if they don't exist
    with app.app_context():
        # Import models so SQLAlchemy knows about them before creating tables
        from app.models.role import Role
        from app.models.user import User
        from app.models.department import Department
        from app.models.employee import Employee
        from app.models.job import Job
        db.create_all()

    return app
