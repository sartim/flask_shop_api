from marshmallow.schema import BaseSchema
from app import ma
from app.permission.models import Permission


class PermissionSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Permission
