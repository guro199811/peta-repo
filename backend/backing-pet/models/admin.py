from db import db


class Admin(db.Model):
    __tablename__ = "admins"

    active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
