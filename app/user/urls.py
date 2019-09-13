from app import app
from app.user.api import GenerateJwtApi, RefreshJwtApi, UserApi, DownloadUserApi, OnlineStatusApi, RoleApi
from app.core.urls import register_api

# user api url rules
app.add_url_rule('/users/generate-jwt', view_func=GenerateJwtApi.as_view('generate-jwt'), methods=['POST'])
app.add_url_rule('/users/refresh-jwt', view_func=RefreshJwtApi.as_view('refresh-jwt'), methods=['POST'])
app.add_url_rule('/users/download', view_func=DownloadUserApi.as_view('users-download'), methods=['GET'])
app.add_url_rule('/users/online', view_func=OnlineStatusApi.as_view('users-online'), methods=['GET'])
# user role api rules
app.add_url_rule('/users/roles', view_func=RoleApi.as_view('users-roles-list'), methods=['GET', 'POST'])
app.add_url_rule('/users/roles/<id>', view_func=RoleApi.as_view('users-roles-detail'), methods=['GET', 'DELETE'])
register_api(UserApi, 'user_api', '/users/', pk='user_id')
