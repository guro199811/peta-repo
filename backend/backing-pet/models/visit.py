from db import db


class Visit(db.Model):
    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    vet_id = db.Column(db.Integer, db.ForeignKey("vets.vet_id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    owner_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)

    def to_dict(self):
        return {
            self.visit_id: {
                "clinic_id": self.clinic_id,
                "vet_id": self.vet_id,
                "pet_id": self.pet_id,
                "owner_id": self.owner_id,
                "diagnosis": self.diagnosis,
                "treatment": self.treatment,
                "comment": self.comment,
                "date": self.date,
                "clinic": self.clinic.to_dict(),
                "vet": self.vet.to_dict(),
                "pet": self.pet.to_dict(),
                "pet_owner": self.pet_owner.to_dict()
            }
        }
