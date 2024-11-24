from db import db


class PetSpecies(db.Model):
    __tablename__ = "pet_species"

    species_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species = db.Column(db.String(50))
    breeds = db.relationship("PetBreed", back_populates="species")

    def to_dict(self):
        return {
            "species_id": self.species_id,
            "species": self.species,
            "breeds": [breed.to_dict() for breed in self.breeds],
        }