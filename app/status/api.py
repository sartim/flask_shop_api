from app.core.base_resource import UnauthorizedBaseResource
from app.status.models import Status
from app.status.schemas import StatusSchema, status_args_schema


class StatusApi(UnauthorizedBaseResource):
    schema = StatusSchema
    model = Status
    request_args = status_args_schema
