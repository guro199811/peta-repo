from db import db


class Pet(db.Model):
    """
    A Pet represents an animal owned by a Owner(person).
    It contains information of the species, breed, gender, medical condition,
    current treatment, recent vaccination, name, birth date, and owner.
    """

    __tablename__ = "pets"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_species = db.Column(
        db.Integer, db.ForeignKey("pet_species.species_id")
    )
    species = db.relationship("PetSpecies")
    pet_breed = db.Column(db.Integer, db.ForeignKey("pet_breeds.breed_id"))
    breed = db.relationship("PetBreed")
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    recent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship("Owner")
