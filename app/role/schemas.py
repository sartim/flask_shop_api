from app.core.app import ma
from webargs import fields
from app.core.base_schema import (
    AbstractBaseSchema, BaseSchema, base_args_schema)
from app.permission.schemas import PermissionSchema
from app.role.models import Role, RolePermission


class RolePermissionSchema(ma.SQLAlchemySchema, AbstractBaseSchema):
    role_id = ma.Str(required=True)
    permission_id = ma.Str(required=True)

    permission = ma.Nested(
        PermissionSchema(only=('name', 'description',)))

    class Meta:
        model = RolePermission
        load_instance = True


class RoleSchema(ma.SQLAlchemySchema, BaseSchema):
    name = ma.Str(required=True)
    description = ma.Str()

    class Meta:
        model = Role


role_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "description": fields.Str(),
    "deleted": fields.Boolean()
}
role_args_schema = {**base_args_schema, **role_args_schema}
