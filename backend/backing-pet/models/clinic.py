from db import db


class Clinic(db.Model):
    __tablename__ = "clinics"

    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person = db.relationship("PersonClinic", lazy="dynamic")
    clinic_name = db.Column(db.String(200))
    desc = db.Column(db.String(201))
    coordinates = db.Column(db.String(75))
    visibility = db.Column(db.Boolean, default=True)
