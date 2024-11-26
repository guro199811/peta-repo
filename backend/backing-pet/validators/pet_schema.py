from marshmallow import Schema, fields


class PetSchema(Schema):
    pet_id = fields.Integer(dump_only=True)
    pet_species = fields.Integer()
    pet_breed = fields.Integer()
    gender = fields.String()
    medical_condition = fields.String(required=False, allow_none=True)
    current_treatment = fields.String(required=False, allow_none=True)
    recent_vaccination = fields.Date(required=False, allow_none=True)
    name = fields.String()
    birth_date = fields.Date()
    owner_id = fields.Integer()
