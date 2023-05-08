from marshmallow import fields
from webargs import fields as fd


class AbstractBaseSchema:
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S', dump_only=True)
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S', dump_only=True)


class BaseSchema(AbstractBaseSchema):
    id = fields.Str()


base_args_schema = {
    "page": fd.Int(),
    "limit": fd.Int(),
    "created_at": fd.DateTime(),
    "updated_at": fd.DateTime()
}
