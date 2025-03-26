from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Boolean, ForeignKey

from db import Base


class Vet(Base):
    __tablename__ = "vets"

    active: Mapped[bool] = mapped_column(Boolean, default=True)
    vet_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
    person_data = relationship("Person", lazy="joined")
    has_license: Mapped[bool] = mapped_column(Boolean, default=False)
    temporary_license: Mapped[bool] = mapped_column(Boolean, default=True)

    def to_dict(self):
        return {
                "vet_id": self.vet_id,
                "person_data": self.person_data.to_dict(),
                "has_license": self.has_license,
                "temporary_license": self.temporary_license,
                "active": self.active,
            }

    def __repr__(self):
        return f"{self.to_dict()}"
