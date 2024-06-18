from db import db


class UserRequests(db.Model):
    __tablename__ = "user_requests"
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_type = db.Column(db.String(20))
    requester_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    reciever_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    request_sent = db.Column(db.Date)
    comment = db.Column(db.String(100), nullable=True)
    ref = db.Column(db.Integer, nullable=True)
    requester = db.relationship(
        "Person", foreign_keys=[requester_id], backref="sent_requests"
    )

    reciever = db.relationship(
        "Person", foreign_keys=[reciever_id], backref="received_requests"
    )
    approved = db.Column(db.Boolean, default=False, nullable=True)
