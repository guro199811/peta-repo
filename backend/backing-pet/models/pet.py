from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from datetime import date
from typing import Optional

from db import Base


class Pet(Base):
    __tablename__ = "pets"

    pet_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pet_species: Mapped[int] = mapped_column(ForeignKey("pet_species.species_id"))
    species = relationship("PetSpecies", lazy="joined")
    pet_breed: Mapped[int] = mapped_column(ForeignKey("pet_breeds.breed_id"))
    breed = relationship("PetBreed", lazy="joined")
    gender: Mapped[str] = mapped_column(String(10))
    medical_condition: Mapped[str] = mapped_column(String(50))
    current_treatment: Mapped[str] = mapped_column(String(50))
    recent_vaccination: Mapped[Optional[date]] = mapped_column(Date)
    name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
    owner = relationship("Person", lazy="joined")

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "pet_species": {
                "species": self.species.species,
                "species_id": self.species.species_id,
            },
            "pet_breed": {"breed": self.breed.breed, "breed_id": self.breed.breed_id},
            "gender": self.gender,
            "medical_condition": self.medical_condition,
            "current_treatment": self.current_treatment,
            "recent_vaccination": self.recent_vaccination,
            "name": self.name,
            "birth_date": self.birth_date,
            "owner": self.owner.to_dict(),
        }

    def __repr__(self):
        return f"{self.to_dict()}"
