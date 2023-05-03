from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource, ChildBaseResource
from app.role.models import Role, RolePermission
from app.role.schemas import RoleSchema, role_args_schema, RolePermissionSchema


class RoleApi(BaseResource):
    schema = RoleSchema
    model = Role
    request_args = role_args_schema


class RolePermissionApi(ChildBaseResource):
    decorators = [cross_origin(), jwt_required()]
    parent = Role
    field = "role_id"
    model = RolePermission
    schema = RolePermissionSchema
