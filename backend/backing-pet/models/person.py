from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey, DateTime, String
from datetime import datetime

from db import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_prefix: Mapped[str] = mapped_column(String(10), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    mail: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created: Mapped[str] = mapped_column(DateTime)
    user_type: Mapped[int] = mapped_column(Integer, ForeignKey("user_types.user_type"))
    person_type = relationship("UserType", lazy="joined")
    password: Mapped[str] = mapped_column(String, nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    confirmed_on: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    temporary_block: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "phone": self.phone,
            "mail": self.mail,
            "address": self.address,
            "created": self.created,
            "user_type": self.user_type,
            "confirmed": self.confirmed,
            "temporary_block": self.temporary_block,
        }

    def __repr__(self):
        return f"{self.to_dict()}"
