from app.core.urls import register_api
from app.status.api import StatusApi

register_api(StatusApi, 'status_api', '/statuses/', pk='status_id')
