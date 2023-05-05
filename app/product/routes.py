from app.product.api import ProductApi
from app.core.helpers.register_helper import register_api

register_api(ProductApi, 'product_api', '/api/v1/products', pk='_id')
