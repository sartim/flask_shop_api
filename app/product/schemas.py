from marshmallow.schema import BaseSchema

from app.core.app import ma
from app.product.models import Product


class ProductSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Product
