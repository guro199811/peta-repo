from db import db


class Clinic(db.Model):
    __tablename__ = "clinics"

    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_name = db.Column(db.String(200))
    desc = db.Column(db.String(201))
    coordinates = db.Column(db.String(75))
    visibility = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "clinic_id": self.clinic_id,
            "clinic_name": self.clinic_name,
            "desc": self.desc,
            "coordinates": self.coordinates,
            "visibility": self.visibility,
        }
