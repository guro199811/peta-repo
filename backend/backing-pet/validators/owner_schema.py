from marshmallow import Schema, fields


class OwnerSchema(Schema):
    id = fields.IntegerField(dump_only=True)
    person_id = fields.IntegerField(required=True)