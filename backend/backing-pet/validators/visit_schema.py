from marshmallow import Schema, fields
from datetime import datetime


class VisitSchema(Schema):
    visit_id = fields.Integer(dump_only=True)
    clinic_id = fields.Integer(required=True)
    vet_id = fields.Integer()
    pet_id = fields.Integer(required=True)
    diagnosis = fields.String()
    treatment = fields.String()
    comment = fields.String()
    date = fields.Date(default=datetime.now())


class VisitAddSchema(Schema):
    clinic_id = fields.Integer(required=True)
    pet_id = fields.Integer(required=True)
    diagnosis = fields.String()
    treatment = fields.String()
    comment = fields.String()
    date = fields.Date(default=datetime.now())
