from db import db


class PersonClinic(db.Model):
    __tablename__ = "bridges"

    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person_data = db.relationship("Person", lazy="joined")
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship("Clinic", lazy="joined")
    is_clinic_owner = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "bridge_id": self.bridge_id,
            "person_data": self.person_data.to_dict(),
            "clinic": self.clinic.to_dict(),
            "is_clinic_owner": self.is_clinic_owner,
        }
