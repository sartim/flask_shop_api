from app.status.api import StatusApi
from app.core.helpers.register_helper import register_api

register_api(StatusApi, 'status_api', '/statuses', pk='id')
