from app.core.base_resource import BaseResource
from app.status.models import Status
from app.status.schemas import StatusSchema, status_args_schema


class StatusApi(BaseResource):
    schema = StatusSchema
    model = Status
    request_args = status_args_schema
