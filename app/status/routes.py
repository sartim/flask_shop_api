from flask import Blueprint
from app.status.api import StatusApi
from app.core.helpers.register_helper import register_api

status_api = Blueprint('status_api', __name__)

register_api(status_api, StatusApi, 'status_api', '/statuses', pk='_id')
