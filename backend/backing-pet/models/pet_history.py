from db import db


class PetHistory(db.Model):
    __tablename__ = "pet_history"

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(
        db.Integer, db.ForeignKey("clinics.clinic_id"), nullable=True
    )
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))
