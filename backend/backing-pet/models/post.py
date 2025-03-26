from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, ForeignKey
from datetime import datetime

from db import Base


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    posted: Mapped[datetime] = mapped_column(DateTime)
    editor_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
