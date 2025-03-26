from sqlalchemy.orm import (
    Mapped, mapped_column
)
from sqlalchemy import (
    Integer, String, DateTime, ForeignKey
)
from datetime import datetime

from db import Base


class Note(Base):
    __tablename__ = "notes"

    note_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[int]  = mapped_column(Integer, ForeignKey("persons.id"))
    created: Mapped[datetime] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(String(500))
