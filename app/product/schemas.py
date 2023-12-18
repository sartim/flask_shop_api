from marshmallow import fields
from app.core.app import ma
from app.product.models import Product
from app.core.base_schema import (base_args_schema, BaseSchema)
from app.category.schemas import CategorySchema


class ProductSchema(ma.SQLAlchemySchema, BaseSchema):
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    items = fields.Int(required=True)
    image_urls = fields.Str()
    price = fields.Float(required=True)
    category_id = fields.Str(required=True)
    deleted = fields.Bool()
    category = fields.Nested(CategorySchema())


    class Meta:
        model = Product
        load_instance = True


product_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "brand": fields.Str(),
}
variant_args_schema = {**base_args_schema, **product_args_schema}
