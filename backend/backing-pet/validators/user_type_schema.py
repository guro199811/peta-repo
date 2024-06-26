from marshmallow import Schema, fields


class UserTypeSchema(Schema):
    user_type = fields.Integer()
    desc = fields.String()