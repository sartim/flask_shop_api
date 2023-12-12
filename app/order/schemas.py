from marshmallow import fields
from marshmallow.schema import BaseSchema
from app.core.app import ma
from app.order.models import Order, OrderItem
from app.core.base_schema import base_args_schema


class OrderItemSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = OrderItem


class OrderSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Order


order_item_args_schema = {
    "order_id": fields.Int(),
    "product_id": fields.Str(),
}
order_item_args_schema = {**base_args_schema, **order_item_args_schema}


order_args_schema = {
    "user_id": fields.Str(),
    "status_id": fields.Str(),
}
order_args_schema = {**base_args_schema, **order_args_schema}
