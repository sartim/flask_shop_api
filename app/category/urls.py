from app.category.api import CategoryApi
from app.core.urls import register_api

register_api(CategoryApi, 'category_api', '/categories', pk='category_id')