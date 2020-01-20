from marshmallow import fields, Schema


class AuthSchema(Schema):
    phone = fields.Str()
    email = fields.Email()
    password = fields.Str(required=True)
