from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.base_resource import BaseResource
from app.order.models import Order, OrderItem
from app.order.schemas import OrderSchema, OrderItemSchema


class OrderApi(BaseResource):
    decorators = [cross_origin(), jwt_required]
    model = Order
    schema = OrderSchema


class OrderItemApi(BaseResource):
    decorators = [cross_origin(), jwt_required]
    model = OrderItem
    schema = OrderItemSchema


class OrderTotalSumTodayApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        data = Order.get_today_sum()
        return self.response(data)


class OrderCountApi(BaseResource):
    # decorators = [cross_origin(), jwt_required]
    def get(self, period=None):
        orders = Order.get_orders_by_filter(period)
        return self.response(orders)
