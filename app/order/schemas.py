from marshmallow.schema import BaseSchema

from app import ma
from app.order.models import Order, OrderItem


class OrderItemSchema(ma.ModelSchema, BaseSchema):
    class Meta:
        model = OrderItem



class OrderSchema(ma.ModelSchema, BaseSchema):
    class Meta:
        model = Order
