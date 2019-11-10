from app.core.urls import register_api
from app.permission.api import PermissionApi

register_api(
    PermissionApi, 'permission_api',
    '/permissions/', pk='permission_id'
)
