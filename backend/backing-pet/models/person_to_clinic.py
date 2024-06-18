from db import db


class PersonToClinic(db.Model):
    __tablename__ = "bridges"
    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship("Person")
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship("Clinic")
    is_clinic_owner = db.Column(db.Boolean, default=False)
