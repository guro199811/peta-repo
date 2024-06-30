from db import db


class UserRequests(db.Model):
    __tablename__ = "user_requests"
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_type = db.Column(db.String(20))
    requester_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    reciever_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    request_sent = db.Column(db.Date)
    comment = db.Column(db.String(100), nullable=True)
    ban = db.Column(db.Integer, nullable=False, default=False)

    requester = db.relationship("Person", lazy="joined")
    reciever = db.relationship("Person", lazy="joined")

    approved = db.Column(db.Boolean, default=False, nullable=True)

    reference_id = db.Column(db.Integer, nullable=True)

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
