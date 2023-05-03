from app.core.helpers.register_helper import register_api
from app.role.api import RoleApi

register_api(RoleApi, 'role_api', '/roles', pk='_id')
