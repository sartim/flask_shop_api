from app.core.app import ma
from webargs import fields
from app.core.base_schema import BaseSchema, base_args_schema
from app.permission.models import Permission


class PermissionSchema(ma.SQLAlchemySchema, BaseSchema):
    name = ma.Str(required=True)
    description = ma.Str()
    path = ma.Str()

    class Meta:
        model = Permission
        load_instance = True


permission_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "description": fields.Str(),
    "path": fields.Str(),
    "deleted": fields.Boolean()
}
permission_args_schema = {**base_args_schema, **permission_args_schema}
