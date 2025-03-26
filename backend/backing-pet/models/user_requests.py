from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime

from db import Base


class UserRequests(Base):
    __tablename__ = "user_requests"
    request_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_type: Mapped[str] = mapped_column(String(20))
    requester_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
    reciever_id: Mapped[int] = mapped_column(Integer, ForeignKey("persons.id"))
    request_sent: Mapped[datetime] = mapped_column(DateTime)
    comment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ban: Mapped[int] = mapped_column(Integer, nullable=False, default=False)

    requester = relationship(
        "Person", foreign_keys=[requester_id], lazy="joined")
    reciever = relationship(
        "Person", foreign_keys=[reciever_id], lazy="joined")

    approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    reference_id: Mapped[int] = mapped_column(Integer, nullable=True)

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "request_type": self.request_type,
            "requester": self.requester.to_dict(),
            "reciever": self.reciever.to_dict(),
            "request_sent": self.request_sent,
            "comment": self.comment,
            "ref": self.ref,
            "approved": self.approved,
        }
