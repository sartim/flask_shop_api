from app.core.base_resource import BaseResource
from app.category.models import Category
from app.category.schemas import CategorySchema, category_args_schema


class CategoryApi(BaseResource):
    model = Category
    schema = CategorySchema
    request_args = category_args_schema
