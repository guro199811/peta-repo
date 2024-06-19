from db import db


class PersonClinic(db.Model):
    __tablename__ = "bridges"

    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person_data = db.relationship("Person", lazy="dynamic")
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship("Clinic", lazy="dynamic")
    is_clinic_owner = db.Column(db.Boolean, default=False)
