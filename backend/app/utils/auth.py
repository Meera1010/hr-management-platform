from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app.models.role import Role

def _get_user_by_identity(identity):
    if identity is None:
        return None
    try:
        return User.query.get(int(identity))
    except (ValueError, TypeError):
        return User.query.get(identity)

def get_current_user():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return _get_user_by_identity(user_id)

def token_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = _get_user_by_identity(user_id)
        if not current_user or not current_user.is_active:
            return jsonify({"success": False, "message": "Authentication required"}), 401
        return fn(current_user, *args, **kwargs)
    return wrapper

def role_required(*allowed_roles):
    # Flatten if passed list e.g. role_required(['Admin', 'HR'])
    roles_set = set()
    for item in allowed_roles:
        if isinstance(item, (list, tuple, set)):
            roles_set.update(item)
        else:
            roles_set.add(item)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = _get_user_by_identity(user_id)
            
            if not user or not user.is_active:
                return jsonify({"success": False, "message": "Authentication required"}), 401
                
            if not user.role or user.role.name not in roles_set:
                return jsonify({"success": False, "message": "You do not have permission to access this resource"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Specific Role Decorators
def admin_required():
    return role_required('Admin')

def hr_required():
    return role_required('Admin', 'HR')

def recruiter_required():
    return role_required('Admin', 'HR', 'Recruiter')

def employee_required():
    return role_required('Admin', 'HR', 'Employee')

def candidate_required():
    return role_required('Admin', 'HR', 'Recruiter', 'Candidate')

def interviewer_required():
    return role_required('Admin', 'HR', 'Recruiter', 'Interviewer')
