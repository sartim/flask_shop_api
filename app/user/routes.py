from flask import Blueprint
from app.user.api import (UserApi, DownloadUserApi, OnlineStatusApi)
from app.core.helpers.register_helper import register_basic_api, register_api

user_api = Blueprint('user_api', __name__)

register_basic_api(
    user_api, DownloadUserApi, 'download_users_api',
    '/api/v1/users/download', methods=['POST']
)
register_basic_api(
    user_api, OnlineStatusApi, 'users_online_api',
    '/api/v1/users/online', methods=['POST']
)
register_api(
    user_api, UserApi, 'user_api', '/api/v1/users', pk='_id')
