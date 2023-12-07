from flask import Blueprint

from app.order.api import (
    OrderApi, OrderTotalSumTodayApi, OrderCountApi, OrderItemApi
)
from core.helpers.register_helper import register_api, register_basic_api

order_api = Blueprint('order_api', __name__)

register_api(
    order_api, OrderApi,
    'order_api',
    '/api/v1/orders',
    pk='_id'
)
register_basic_api(
    order_api, OrderTotalSumTodayApi,
    'order_total_sum_today_api',
    '/api/v1/orders/total-sum'
)
register_basic_api(
    order_api, OrderCountApi,
    'order_count_api',
    '/api/v1/orders/<string:period>/count'
)
register_basic_api(
    order_api, OrderItemApi,
    'order_items_api',
    '/api/v1/orders/items',
    methods=['POST']
)
