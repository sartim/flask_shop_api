from app.user.api import (UserApi, DownloadUserApi, OnlineStatusApi)
from app.core.helpers.register_helper import register_basic_api, register_api

register_basic_api(
    DownloadUserApi, 'download_users_api',
    '/api/v1/users/download', methods=['POST']
)
register_basic_api(
    OnlineStatusApi, 'users_online_api',
    '/api/v1/users/online', methods=['POST']
)
register_api(UserApi, 'user_api', '/api/v1/users', pk='_id')
