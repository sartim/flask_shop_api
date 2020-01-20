from marshmallow.schema import BaseSchema

from app import ma
from app.product.models import Product


class ProductSchema(ma.ModelSchema, BaseSchema):
    class Meta:
        model = Product
