from marshmallow import Schema, fields


class RequestSchema(Schema):
    request_id = fields.Integer(dump_only=True)
    request_type = fields.String(required=True)
    requester_id = fields.Integer(required=True)
    reciever_id = fields.Integer(required=True)
    request_sent = fields.Date(required=True)
    comment = fields.String()
    ban = fields.Boolean()
    approved = fields.Boolean(default=False)


class ApprovealRequestSchema(Schema):
    request_id = fields.Integer(dump_only=True)
    approved = fields.Boolean(default=False)
