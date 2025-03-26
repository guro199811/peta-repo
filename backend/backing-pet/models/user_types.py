from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from db import Base


class UserType(Base):
    __tablename__ = "user_types"

    user_type: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    desc: Mapped[str] = mapped_column(String(50))

    def to_dict(self):
        return {
            "user_type": self.user_type,
            "description": self.desc,
        }
