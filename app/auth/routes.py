from app.auth.api import GenerateJwtApi, RefreshJwtApi
from app.core.helpers.register_helper import register_basic_api

register_basic_api(
    GenerateJwtApi, 'generate_jwt_api',
    '/api/v1/auth/generate-jwt', methods=['POST']
)
register_basic_api(
    RefreshJwtApi, 'refresh_jwt_api',
    '/api/v1/auth/refresh-jwt',  methods=['POST']
)
