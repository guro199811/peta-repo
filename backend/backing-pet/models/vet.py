from db import db


class Vet(db.Model):
    __tablename__ = "vets"

    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    has_license = db.Column(db.Boolean, default=False)
    temporary_license = db.Column(db.Boolean, default=False)
