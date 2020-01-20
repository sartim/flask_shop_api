from app.core.helpers.register_helper import register_api
from app.permission.api import PermissionApi

register_api(
    PermissionApi, 'permission_api',
    '/permissions', pk='id'
)
