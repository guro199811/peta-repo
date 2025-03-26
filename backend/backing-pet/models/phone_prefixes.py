from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from db import Base


class PhonePrefixes(Base):
    __tablename__ = "phone_prefixes"

    prefix_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    prefix: Mapped[str] = mapped_column(String(10), unique=True)
    nums: Mapped[int] = mapped_column(Integer)
    icon: Mapped[str] = mapped_column(String(10), nullable=False, default="&#127987")
