from app import app
from app.core.urls import register_api
from app.product.api import ProductApi, ProductCategoryApi, DownloadProductApi, DownloadProductCategoryApi

# product api url rules
register_api(ProductApi, 'provider_api', '/products/', pk='product_id')
app.add_url_rule('/products/download', view_func=DownloadProductApi.as_view('products-download'), methods=['GET'])

# product category api url rules
register_api(ProductCategoryApi, 'product_category_api', '/categories/', pk='category_id')
app.add_url_rule('/products/category/download',
                 view_func=DownloadProductCategoryApi.as_view('product-categories-download'), methods=['GET'])
