from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource
from app.category.models import Category
from app.category.schemas import CategorySchema


class CategoryApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]
    model = Category
    schema = CategorySchema
