from marshmallow import fields
from marshmallow.schema import BaseSchema
from app.core.app import ma
from app.product.models import Product
from app.core.base_schema import base_args_schema


class ProductSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Product


product_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "brand": fields.Str(),
}
variant_args_schema = {**base_args_schema, **product_args_schema}
