from app import ma
from webargs import fields
from app.core.base_schema import (
    AbstractBaseSchema, BaseSchema, base_args_schema)
from app.status.models import Status


class StatusSchema(ma.SQLAlchemySchema, BaseSchema):
    name = ma.Str(required=True)
    description = ma.Str()

    class Meta:
        model = Status


status_args_schema = {
    "id": fields.Str(),
    "name": fields.Str(),
    "description": fields.Str(),
    "deleted": fields.Boolean()
}
status_args_schema = {**base_args_schema, **status_args_schema}
