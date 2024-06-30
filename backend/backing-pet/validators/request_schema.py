from marshmallow import Schema, fields


class PlainRequestSchema(Schema):
    request_id = fields.Integer(dump_only=True)


class RequestSchema(PlainRequestSchema):
    request_type = fields.String()
    requester_id = fields.Integer()
    reciever_id = fields.Integer()
    request_sent = fields.Date(required=True)
    comment = fields.String()
    ban = fields.Boolean()
    approved = fields.Boolean(default=False)


class ApprovealRequestSchema(Schema):
    request_id = fields.Integer(dump_only=True)
    approved = fields.Boolean(default=False)


class ClinicRequestSchema(RequestSchema):
    reference_id = fields.Integer(required=True)


class ClinicApprovalRequestSchema(Schema):
    request_id = fields.Integer(required=True)
    approved = fields.Boolean(required=True)
    reference_id = fields.Integer(required=True)
