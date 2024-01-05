from app.core.base_resource import UnauthorizedBaseResource
from app.category.models import Category
from app.category.schemas import CategorySchema, category_args_schema


class CategoryApi(UnauthorizedBaseResource):
    model = Category
    schema = CategorySchema
    request_args = category_args_schema
