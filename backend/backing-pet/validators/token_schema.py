from marshmallow import Schema, fields


class TokenSchema(Schema):
    message = fields.String()
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    token_type = fields.String(required=True)
