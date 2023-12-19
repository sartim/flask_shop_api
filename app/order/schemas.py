from marshmallow import fields
from app.core.app import ma
from app.order.models import Order, OrderItem
from app.core.base_schema import base_args_schema, BaseSchema
from app.product.schemas import ProductSchema
from app.status.schemas import StatusSchema
from app.user.schemas import UserSchema


class OrderItemSchema(ma.SQLAlchemySchema, BaseSchema):
    product = fields.Nested(ProductSchema())
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)

    class Meta:
        model = OrderItem


class OrderSchema(ma.SQLAlchemySchema, BaseSchema):
    id = fields.Int()
    user_id = fields.Str(required=True)
    status_id = fields.Str(required=True)
    order_total = fields.Float(required=True)

    user = fields.Nested(UserSchema())
    status = fields.Nested(StatusSchema())

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
