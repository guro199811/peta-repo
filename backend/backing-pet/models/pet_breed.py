from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from db import Base


class PetBreed(Base):
    __tablename__ = "pet_breeds"

    breed_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    species_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pet_species.species_id")
    )
    breed: Mapped[str] = mapped_column(String(100))

    species = relationship("PetSpecies", back_populates="breeds")

    def to_dict(self):
        return {
            "breed_id": self.breed_id,
            "species_id": self.species_id,
            "species": self.species.species,
            "breed": self.breed,
        }