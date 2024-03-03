from marshmallow import fields
from app.core.app import ma
from app.category.models import Category
from app.core.base_schema import (BaseSchema, base_args_schema)


class CategorySchema(ma.SQLAlchemySchema, BaseSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    deleted = fields.Bool()

    class Meta:
        model = Category

category_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "description": fields.Str(),
    "deleted": fields.Boolean()
}
category_args_schema = {**base_args_schema, **category_args_schema}
