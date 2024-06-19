from db import db


class Note(db.Model):
    __tablename__ = "notes"

    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship("Person", lazy="dynamic")
    created = db.Column(db.Date)
    content = db.Column(db.String(500))
