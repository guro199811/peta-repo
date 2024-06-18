from db import db


class Note(db.Model):
    """
    A Note represents a note or a remark made by a person.
    It contains information about the person who made the note,
    the date when the note was created, and the content of the note.
    """

    __tablename__ = "notes"
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship("Person")
    created = db.Column(db.Date)
    content = db.Column(db.String(500))
