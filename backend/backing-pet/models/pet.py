from db import db


class Pet(db.Model):
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
    owner_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    pet_owner = db.relationship("Person")

    def to_dict(self):
        return {self.pet_id: {
            "pet_species": self.pet_species,
            "pet_breed": self.pet_breed,
            "gender": self.gender,
            "medical_condition": self.medical_condition,
            "current_treatment": self.current_treatment,
            "recent_vaccination": self.recent_vaccination,
            "name": self.name,
            "birth_date": self.birth_date,
            "owner_id": self.owner_id,
            "pet_owner": self.pet_owner.to_dict()
        }}
