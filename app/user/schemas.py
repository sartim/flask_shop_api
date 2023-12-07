from marshmallow import fields
from webargs import fields as fd
from app.core.app import ma
from app.core.base_schema import AbstractBaseSchema, BaseSchema, \
    base_args_schema
from app.permission.schemas import PermissionSchema
from app.role.schemas import RoleSchema
from app.user.models import User, UserRole, UserPermission


class UserRoleSchema(ma.SQLAlchemySchema, AbstractBaseSchema):
    role_id = ma.Str(required=True)

    role = ma.Nested(RoleSchema(only=('name', 'description',)))

    class Meta:
        model = UserRole
        load_instance = True


class UserPermissionSchema(ma.SQLAlchemySchema, AbstractBaseSchema):
    permission_id = ma.Str(required=True)

    permission = ma.Nested(PermissionSchema(only=('name', 'description',)))

    class Meta:
        model = UserPermission
        load_instance = True


class UserSchema(ma.SQLAlchemySchema, BaseSchema):
    id = fields.String()
    permissions = ma.List(ma.Nested(UserPermissionSchema(only=('permission',))))
    roles = ma.List(ma.Nested(UserRoleSchema(only=('role',))))

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone',
            'is_verified', 'is_active', 'roles', 'organizations', 'image',
            'created_at', 'updated_at', 'meta'
        )
        load_instance = True


user_args_schema = {
    "id": fd.Str(),
    "first_name": fd.Str(),
    "last_name": fd.Str(),
    "email": fd.Str(),
    "phone": fd.Str(),
    "is_active": fd.Boolean(),
    "deleted": fd.Boolean(),
    "role_id": fd.Str()
}
user_args_schema = {**base_args_schema, **user_args_schema}
