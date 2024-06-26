from marshmallow import Schema, fields


class ClinicSchema(Schema):
    clinic_id = fields.Integer(dump_only=True)
    clinic_name = fields.String(required=True)
    desc = fields.String(required=True)
    coordinates = fields.String(required=True)
    visibility = fields.String()
