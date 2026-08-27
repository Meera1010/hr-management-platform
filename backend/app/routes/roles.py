from flask import Blueprint
from app.models.role import Role
from app.utils.responses import success_response, error_response
from app.utils.auth import hr_required

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/', methods=['GET'])
@hr_required()
def get_roles():
    try:
        roles = Role.query.all()
        return success_response("Roles retrieved successfully", [role.to_dict() for role in roles])
    except Exception as e:
        return error_response("Failed to retrieve roles", 500)

@roles_bp.route('/<int:role_id>', methods=['GET'])
@hr_required()
def get_role(role_id):
    try:
        role = Role.query.get(role_id)
        if not role:
            return error_response("Role not found", 404)
        return success_response("Role retrieved successfully", role.to_dict())
    except Exception as e:
        return error_response("Failed to retrieve role", 500)
