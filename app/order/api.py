from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource, ChildBaseResource
from app.order.models import Order, OrderItem
from app.order.schemas import (
    OrderSchema, OrderItemSchema, order_item_args_schema, order_args_schema)


class OrderApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]
    model = Order
    schema = OrderSchema
    request_args = order_item_args_schema


class OrderItemApi(ChildBaseResource):
    decorators = [cross_origin(), jwt_required()]
    schema = OrderItemSchema
    model = OrderItem
    field = 'order_id'
    parent = Order


class OrderTotalSumTodayApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]

    def get(self, _id=None):
        data = Order.get_today_sum()
        return self.response(data)


class OrderCountApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, _id=None):
        orders = Order.get_orders_by_filter(_id)
        return self.response(orders)
