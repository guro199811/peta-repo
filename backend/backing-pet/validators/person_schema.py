from marshmallow import Schema, fields


class PlainPersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    mail = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PersonSchema(PlainPersonSchema):
    repeat_password = fields.String(required=True)
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    prefix = fields.String(required=True)
    phone = fields.Integer(required=True)
    address = fields.String(required=True)
    user_type = fields.Integer(required=True)
