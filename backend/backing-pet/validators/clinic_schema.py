from marshmallow import Schema, fields


class ClinicSchema(Schema):
    clinic_id = fields.Integer(dump_only=True)
    clinic_name = fields.String(required=True)
    desc = fields.String(required=True)
    coordinates = fields.String(required=True)
    visibility = fields.Boolean(default=False)


class PersonToClinicSchema(Schema):
    bridge_id = fields.Integer(dump_only=True)
    person_id = fields.Integer(required=True)
    clinic_id = fields.Integer(required=True)
    is_clinic_owner = fields.Boolean(default=False)
