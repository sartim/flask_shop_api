from marshmallow.schema import BaseSchema

from app import ma
from app.category.models import Category


class CategorySchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = Category
