from db import db


class PetSpecies(db.Model):
    __tablename__ = "pet_species"

    species_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species = db.Column(db.String(50))
