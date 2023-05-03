from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource
from app.role.models import Role
from app.role.schemas import RoleSchema


class RoleApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]
    schema = RoleSchema()
    model = Role
