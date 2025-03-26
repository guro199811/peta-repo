from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy import (
    Integer, Boolean, ForeignKey
)

from db import Base

class PersonClinic(Base):
    __tablename__ = "bridges"

    bridge_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
    person_data = relationship("Person", lazy="joined")
    clinic_id: Mapped[int] = mapped_column(Integer, ForeignKey("clinics.clinic_id"))
    clinic = relationship("Clinic", lazy="joined")
    is_clinic_owner: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {
            "bridge_id": self.bridge_id,
            "person_data": self.person_data.to_dict(),
            "clinic": self.clinic.to_dict(),
            "is_clinic_owner": self.is_clinic_owner,
        }
