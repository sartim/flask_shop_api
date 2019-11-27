from app.user.api import UserApi
from app.core.urls import register_api

register_api(UserApi, 'user_api', '/users', pk='user_id')
