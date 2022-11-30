from app import ma
from app.core.base_schema import BaseSchema
from app.permission.schemas import PermissionSchema
from app.role.models import Role, RolePermission


class RolePermissionSchema(ma.SQLAlchemySchema, BaseSchema):
    permission = ma.Nested(PermissionSchema())

    class Meta:
        model = RolePermission


class RoleSchema(ma.SQLAlchemySchema, BaseSchema):
    # permissions = ma.List(ma.Nested(RolePermissionSchema()))

    class Meta:
        model = Role
