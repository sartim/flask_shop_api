from app import app
from app.core.urls import register_api
from app.order.api import OrderApi, OrderCountApi, OrderItemApi

register_api(OrderApi, 'order_api', '/orders/', pk='order_id')
app.add_url_rule(
    '/orders/<period>/count',
    view_func=OrderCountApi.as_view('order_count_api'),
    methods=['GET']
)
app.add_url_rule(
    '/order-items',
    view_func=OrderItemApi.as_view('order-items-create'),
    methods=['POST']
)
