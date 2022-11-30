from marshmallow.schema import BaseSchema

from app import ma
from app.order.models import Order, OrderItem


class OrderItemSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = OrderItem


class OrderSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Order
