from marshmallow.schema import BaseSchema

from app import ma
from app.category.models import Category


class CategorySchema(ma.ModelSchema, BaseSchema):
    class Meta:
        model = Category
