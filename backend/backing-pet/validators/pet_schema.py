from marshmallow import Schema, fields


class PetSchema(Schema):
    pet_id = fields.Integer(dump_only=True)
    pet_species = fields.Integer(default=1)
    pet_breed = fields.Integer(default=1)
    gender = fields.String(default="M")
    medical_condition = fields.String()
    current_treatment = fields.String()
    recent_vaccination = fields.Date()
    name = fields.String()
    birth_date = fields.Date()
    owner_id = fields.Integer()
