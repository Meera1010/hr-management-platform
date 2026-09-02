from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.models.role import Role
from app import db
from app.utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return error_response('Email and password are required', 400)
        
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return error_response('Invalid credentials', 401)
        
    if not user.is_active:
        return error_response('Authentication required', 401)
        
    if not user.check_password(password):
        return error_response('Invalid credentials', 401)
        
    # Generate access token
    access_token = create_access_token(identity=str(user.id))
    
    return success_response('Login successful', {
        'access_token': access_token,
        'user': {
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'role': user.role.name if user.role else None
        }
    })

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a stateless JWT implementation, logout is primarily handled on the client side
    # by removing the token from local storage.
    # To implement server-side logout securely, we would need a token blocklist (revocation list).
    # For this demo, we simply return success to acknowledge the logout request.
    return success_response('Logout successful')

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    raw_id = get_jwt_identity()
    user_id = int(raw_id) if raw_id is not None else None
    user = User.query.get(user_id) if user_id is not None else None
    
    if not user or not user.is_active:
        return error_response('Authentication required', 401)
        
    return success_response('User retrieved successfully', {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role.name if user.role else None,
        'is_active': user.is_active
    })

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    if not data or not data.get('current_password') or not data.get('new_password'):
        return error_response('Current password and new password are required', 400)
        
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    raw_id = get_jwt_identity()
    user_id = int(raw_id) if raw_id is not None else None
    user = User.query.get(user_id) if user_id is not None else None
    
    if not user or not user.is_active:
        return error_response('Authentication required', 401)
        
    if not user.check_password(current_password):
        return error_response('Invalid credentials', 401)
        
    # Basic validation for new password could go here
    if len(new_password) < 6:
        return error_response('New password must be at least 6 characters long', 400)
        
    user.set_password(new_password)
    db.session.commit()
    
    return success_response('Password changed successfully')
