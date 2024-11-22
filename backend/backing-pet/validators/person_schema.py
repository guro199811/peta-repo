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
    address = fields.String()
    user_type = fields.Integer()


class PersonGetterSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    lastname = fields.String(required=True)
    prefix = fields.String(required=True)
    phone = fields.String(required=True)
    mail = fields.String(required=True)
    address = fields.String()
    created = fields.Date(required=True)
    user_type = fields.Integer()
    temporary_block = fields.Boolean()


class PlainPersonUpdateSchema(Schema):
    name = fields.String()
    lastname = fields.String()
    prefix = fields.String()
    phone = fields.String()
    address = fields.String()


class PersonUpdateSchema(PlainPersonUpdateSchema):
    confirmed = fields.Boolean()


class AdminSpecificUpdateSchema(Schema):
    user_type = fields.Integer()
