from flask import Blueprint

from app.order.api import (
    OrderApi, OrderTotalSumTodayApi, OrderCountApi, OrderItemApi
)
from app.core.helpers.register_helper import (
    register_api, register_basic_api, register_complex_api)

order_api = Blueprint('order_api', __name__)

register_api(
    order_api, OrderApi,
    'order_api',
    '/orders',
    pk='_id'
)
register_basic_api(
    order_api, OrderTotalSumTodayApi,
    'order_total_sum_today_api',
    '/orders/total-sum'
)
register_complex_api(
    order_api, OrderCountApi,
    'order_count_api',
    '/orders',
    '/count'
)
register_complex_api(
    order_api, OrderItemApi,
    'order_item_api',
    '/orders',
    '/items'
)
