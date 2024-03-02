from flask import Blueprint

from app.product.api import ProductApi
from app.core.helpers.register_helper import register_api

product_api = Blueprint('product_api', __name__)

register_api(product_api, ProductApi, 'product_api', '/products', pk='_id')
