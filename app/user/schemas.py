from app import ma
from webargs import fields as fd
from app.core.base_schema import BaseSchema, base_args_schema
from app.role.schemas import RoleSchema
from app.user.models import User, UserRole


class UserRoleSchema(ma.SQLAlchemySchema, BaseSchema):
    # role = ma.Nested(RoleSchema(only=('name', 'description',)))

    class Meta:
        model = UserRole


class UserSchema(ma.SQLAlchemySchema, BaseSchema):
    # roles = ma.List(ma.Nested(UserRoleSchema(only=('role',))))

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'email', 'phone', 'addresses',
            'roles', 'image', 'created_at', 'updated_at'
        )


user_args_schema = {
    "id": fd.Int(),
    "first_name": fd.Str(),
    "last_name": fd.Str(),
    "email": fd.Str(),
    "phone": fd.Str(),
    "is_active": fd.Boolean()
}
user_args_schema = {**base_args_schema, **user_args_schema}