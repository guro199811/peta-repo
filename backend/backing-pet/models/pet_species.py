from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from db import Base


class PetSpecies(Base):
    __tablename__ = "pet_species"

    species_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=False
    )
    species: Mapped[str] = mapped_column(String(50))

    # Relationship without Mapped[] to avoid circular imports
    breeds = relationship("PetBreed", back_populates="species")

    def to_dict(self):
        return {
            "species_id": self.species_id,
            "species": self.species,
            "breeds": [breed.to_dict() for breed in self.breeds],
        }
