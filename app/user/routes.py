from app.user.api import (UserApi, DownloadUserApi, OnlineStatusApi)
from app.core.urls import register_api, register_basic_api

register_basic_api(
    DownloadUserApi, 'download_users_api',
    '/users/download', methods=['POST']
)
register_basic_api(
    OnlineStatusApi, 'users_online_api',
    '/users/online', methods=['POST']
)
register_api(UserApi, 'user_api', '/users', pk='id')
