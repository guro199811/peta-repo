from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime

from db import Base


class Visit(Base):
    __tablename__ = "visits"

    visit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    clinic_id: Mapped[int] = mapped_column(Integer, ForeignKey("clinics.clinic_id"))
    vet_id: Mapped[int] = mapped_column(Integer, ForeignKey("vets.vet_id"))
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.pet_id"))
    diagnosis: Mapped[str] = mapped_column(String(100))
    treatment: Mapped[str] = mapped_column(String(50))
    comment: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime] = mapped_column(DateTime)

    clinic = relationship("Clinic", backref="visits", lazy="joined")
    vet = relationship("Vet", backref="visits", lazy="joined")
    pet = relationship("Pet", backref="visits", lazy="joined")

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "clinic_id": self.clinic_id,
            "vet_id": self.vet_id,
            "pet_id": self.pet_id,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "comment": self.comment,
            "date": self.date,
            "clinic": self.clinic.to_dict() if self.clinic else None,
            "vet": self.vet.person_data.to_dict() if self.vet else None,
            "pet": self.pet.to_dict() if self.pet else None
        }
