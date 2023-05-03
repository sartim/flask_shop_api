from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource
from app.permission.models import Permission
from app.permission.schemas import PermissionSchema


class PermissionApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]
    model = Permission
    schema = PermissionSchema()
