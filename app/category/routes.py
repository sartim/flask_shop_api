from app.category.api import CategoryApi
from app.core.helpers.register_helper import register_api

register_api(CategoryApi, 'category_api', '/api/v1/categories', pk='_id')
