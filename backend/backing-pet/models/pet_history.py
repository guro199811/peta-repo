from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from datetime import datetime

from db import Base


class PetHistory(Base):
    __tablename__ = "pet_history"

    history_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    clinic_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("clinics.clinic_id"), nullable=True
    )
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.pet_id"))
    treatment: Mapped[str] = mapped_column(String(50))
    date: Mapped[datetime] = mapped_column(Date)
    comment: Mapped[str] = mapped_column(String(500))
