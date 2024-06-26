from marshmallow import Schema, fields


class PlainPersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    mail = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PersonRegistrationSchema(PlainPersonSchema):
    repeat_password = fields.String(required=True)
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    prefix = fields.String(required=True)
    phone = fields.Integer(required=True)
    address = fields.String(required=True)
    user_type = fields.Integer(required=True)


class PersonGetterSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    mail = fields.String(required=True)
    address = fields.String(required=True)
    created = fields.Date(required=True)
    user_type = fields.Integer(required=True)
    temporary_block = fields.Boolean(required=True)


class PlainPersonUpdateSchema(Schema):
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    address = fields.String(required=True)


class PersonUpdateSchema(PlainPersonUpdateSchema):
    confirmed = fields.Boolean(required=True)


class AdminSpecificUpdateSchema(Schema):
    user_type = fields.Integer(required=True)
