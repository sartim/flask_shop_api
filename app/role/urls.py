from app.core.urls import register_api
from app.role.api import RoleApi

register_api(RoleApi, 'role_api', '/roles', pk='role_id')
