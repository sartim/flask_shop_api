from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.api import BaseResource
from app.core.helpers.decorators import validate
from app.order.models import Order, OrderItem


class OrderApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, order_id=None):
        page = request.args.get('page')
        status = request.args.get('status')
        if status:
            orders = Order.get_all_by_status_body(status, int(page) if page else None)
            return self.response(orders)
        if order_id is None:
            orders = Order.get_all_data(int(page) if page else None)
            return self.response(orders)
        orders = Order.get_by_id_data(order_id)
        return self.response(orders)

    @validate(['user_id', 'status_id'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        order = Order(**request.json)
        order.create()
        result = dict(order_id=order.id)
        return self.response(result, 201)

    def put(self, order_id=None):
        order = Order.get_by_id(order_id)
        if not order:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Order.update(order_id, **request.json)
        if not updated:
            result = dict(message="Did not update supplier.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, order_id=None):
        order = Order.get_by_id(order_id)
        if not order:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = order.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(order_id))
            return self.response(result)
        result = dict(message="{} Not deleted".format(order_id))
        return self.response(result, 400)


class OrderItemApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    @validate(['order_id', 'product_id', 'price', 'quantity'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        order = OrderItem(**request.json)
        order.create()
        result = dict(message="Successfully saved.")
        return self.response(result, 201)


class OrderCountApi(BaseResource):
    # decorators = [cross_origin(), jwt_required]
    def get(self, period=None):
        orders = Order.get_orders_by_filter(period)
        return self.response(orders)
