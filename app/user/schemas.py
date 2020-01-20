from app import ma
from app.core.base_schema import BaseSchema
from app.role.schemas import RoleSchema
from app.user.models import User, UserRole


class UserRoleSchema(ma.ModelSchema, BaseSchema):
    role = ma.Nested(RoleSchema(only=('name', 'description',)))

    class Meta:
        model = UserRole


class UserSchema(ma.ModelSchema, BaseSchema):
    roles = ma.List(ma.Nested(UserRoleSchema(only=('role',))))

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'email', 'phone', 'addresses',
            'roles', 'image', 'created_at', 'updated_at'
        )
