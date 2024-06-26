from db import db


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posted = db.Column(db.DateTime)
    editor_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
