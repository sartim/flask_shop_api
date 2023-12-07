from flask import Blueprint

from app.category.api import CategoryApi
from app.core.helpers.register_helper import register_api

category_api = Blueprint('category_api', __name__)

register_api(
    category_api, CategoryApi, 'category_api', '/api/v1/categories', pk='_id')
