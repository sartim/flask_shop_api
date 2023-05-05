from app.core.base_resource import BaseResource
from app.permission.models import Permission
from app.permission.schemas import PermissionSchema, permission_args_schema


class PermissionApi(BaseResource):
    model = Permission
    schema = PermissionSchema
    request_args = permission_args_schema
