from db import db


class Owner(db.Model):
    __tablename__ = "owners"
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship("Person")
