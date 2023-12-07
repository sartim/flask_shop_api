from flask import Blueprint

from app.core.helpers.register_helper import register_api
from app.permission.api import PermissionApi

permission_api = Blueprint('permission_api', __name__)

register_api(
    permission_api, PermissionApi, 'permission_api',
    '/api/v1/permissions', pk='_id'
)
