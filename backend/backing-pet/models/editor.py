from db import db


class Editor(db.Model):
    __tablename__ = "editors"

    active = db.Column(db.Boolean, default=True)
    editor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship("Person")
