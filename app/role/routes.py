from flask import Blueprint
from app.core.helpers.register_helper import register_api
from app.role.api import RoleApi

role_api = Blueprint('role_api', __name__)

register_api(role_api, RoleApi, 'role_api', '/roles', pk='_id')
