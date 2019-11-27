from app.core.urls import register_api, register_basic_api
from app.order.api import (
    OrderApi, OrderTotalSumTodayApi, OrderCountApi, OrderItemApi
)

register_api(
    OrderApi,
    'order_api',
    '/orders',
    pk='order_id'
)
register_basic_api(
    OrderTotalSumTodayApi,
    'order_total_sum_today_api',
    '/orders/total-sum'
)
register_basic_api(
    OrderCountApi,
    'order_count_api',
    '/orders/<string:period>/count'
)
register_basic_api(
    OrderItemApi,
    'order_items_api',
    '/orders/items',
    methods=['POST']
)
