from flask import Blueprint

from app.auth.api import GenerateJwtApi, RefreshJwtApi
from app.core.helpers.register_helper import register_basic_api

auth_api = Blueprint('auth_api', __name__)

register_basic_api(
    auth_api, GenerateJwtApi, 'generate_jwt_api',
    '/auth/generate-jwt', methods=['POST']
)
register_basic_api(
    auth_api, RefreshJwtApi, 'refresh_jwt_api',
    '/auth/refresh-jwt',  methods=['POST']
)
