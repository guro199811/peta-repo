from db import db


class Visit(db.Model):
    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    vet_id = db.Column(db.Integer, db.ForeignKey("vets.vet_id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)

    clinic = db.relationship("Clinic", backref="visits", lazy="joined")
    vet = db.relationship("Vet", backref="visits", lazy="joined")
    pet = db.relationship("Pet", backref="visits", lazy="joined")

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "clinic_id": self.clinic_id,
            "vet_id": self.vet_id,
            "pet_id": self.pet_id,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "comment": self.comment,
            "date": self.date,
            "clinic": self.clinic.to_dict() if self.clinic else None,
            "vet": self.vet.person_data.to_dict() if self.vet else None,
            "pet": self.pet.to_dict() if self.pet else None
        }
