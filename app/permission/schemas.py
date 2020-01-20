from marshmallow.schema import BaseSchema

from app import ma
from app.permission.models import Permission


class PermissionSchema(ma.ModelSchema, BaseSchema):
    class Meta:
        model = Permission
