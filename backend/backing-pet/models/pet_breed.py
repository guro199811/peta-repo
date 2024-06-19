from db import db


class PetBreed(db.Model):
    __tablename__ = "pet_breeds"

    breed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species_id = db.Column(
        db.Integer, db.ForeignKey("pet_species.species_id")
    )
    species = db.relationship("PetSpecies", lazy="dynamic")
    breed = db.Column(db.String(100))
