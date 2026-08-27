from flask import Blueprint, request
from app import db
from app.models.user import User
from app.models.role import Role
from app.utils.responses import success_response, error_response
from app.utils.validators import is_valid_email, is_valid_phone, is_strong_password
from app.utils.auth import hr_required, admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@hr_required()
def get_users():
    try:
        users = User.query.all()
        return success_response("Users retrieved successfully", [user.to_dict() for user in users])
    except Exception as e:
        return error_response("Failed to retrieve users", 500)

@users_bp.route('/<int:user_id>', methods=['GET'])
@hr_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        return success_response("User retrieved successfully", user.to_dict())
    except Exception as e:
        return error_response("Failed to retrieve user", 500)

@users_bp.route('/', methods=['POST'])
@hr_required()
def create_user():
    try:
        data = request.get_json()
        
        # Validation
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        role_id = data.get('role_id')

        if not first_name or not first_name.strip():
            return error_response("First name is required")
        if not last_name or not last_name.strip():
            return error_response("Last name is required")
        if not email or not is_valid_email(email):
            return error_response("Valid email is required")
        if phone and not is_valid_phone(phone):
            return error_response("Valid phone format is required")
        if not password or not is_strong_password(password):
            return error_response("Password must be at least 6 characters")
        
        # Role validation
        role = Role.query.get(role_id)
        if not role:
            return error_response("Valid role is required")
            
        # Email uniqueness
        if User.query.filter_by(email=email).first():
            return error_response("Email already exists")

        new_user = User(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip(),
            phone=phone.strip() if phone else None,
            role_id=role_id
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return success_response("User created successfully", new_user.to_dict(), 201)

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create user", 500)

@users_bp.route('/<int:user_id>', methods=['PUT'])
@hr_required()
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)

        data = request.get_json()
        
        if 'first_name' in data:
            if not data['first_name'].strip():
                return error_response("First name cannot be empty")
            user.first_name = data['first_name'].strip()
            
        if 'last_name' in data:
            if not data['last_name'].strip():
                return error_response("Last name cannot be empty")
            user.last_name = data['last_name'].strip()
            
        if 'email' in data:
            email = data['email'].strip()
            if not is_valid_email(email):
                return error_response("Valid email is required")
            # Check if email belongs to someone else
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user_id:
                return error_response("Email already exists")
            user.email = email
            
        if 'phone' in data:
            phone = data['phone'].strip() if data['phone'] else None
            if phone and not is_valid_phone(phone):
                return error_response("Valid phone format is required")
            user.phone = phone
            
        if 'role_id' in data:
            role = Role.query.get(data['role_id'])
            if not role:
                return error_response("Valid role is required")
            user.role_id = data['role_id']
            
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
            
        if 'password' in data and data['password']:
            if not is_strong_password(data['password']):
                return error_response("Password must be at least 6 characters")
            user.set_password(data['password'])

        db.session.commit()
        return success_response("User updated successfully", user.to_dict())

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update user", 500)

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required()
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
            
        # Deactivate instead of permanent delete
        user.is_active = False
        db.session.commit()
        
        return success_response("User deactivated successfully", user.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to deactivate user", 500)
