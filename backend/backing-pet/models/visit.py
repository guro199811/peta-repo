from db import db


class Visit(db.Model):
    """
    A Visit represents a pet visit to a clinic by a vet.
    It contains information about the clinic, vet, pet, owner,
    diagnosis, treatment, comment, and date of the visit.
    """

    __tablename__ = "visits"
    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship("Clinic")
    vet_id = db.Column(db.Integer, db.ForeignKey("vets.vet_id"))
    vet = db.relationship("Vet")
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    pet = db.relationship("Pet")
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship("Owner")
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)
