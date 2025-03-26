from sqlalchemy.orm import (
    Mapped, mapped_column
)
from sqlalchemy import (
    Integer, String, Boolean
)

from db import Base


class Clinic(Base):
    __tablename__ = "clinics"

    clinic_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    clinic_name: Mapped[str] = mapped_column(String(200))
    desc: Mapped[str] = mapped_column(String(201))
    coordinates: Mapped[str] = mapped_column(String(75))
    visibility: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_dict(self):
        return {
            "clinic_id": self.clinic_id,
            "clinic_name": self.clinic_name,
            "desc": self.desc,
            "coordinates": self.coordinates,
            "visibility": self.visibility,
        }
