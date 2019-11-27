from app.auth.api import GenerateJwtApi, RefreshJwtApi
from app.core.urls import register_basic_api

register_basic_api(
    GenerateJwtApi, 'generate_jwt_api',
    '/auth/generate-jwt', methods=['POST']
)
register_basic_api(
    RefreshJwtApi, 'refresh_jwt_api',
    '/auth/refresh-jwt',  methods=['POST']
)
