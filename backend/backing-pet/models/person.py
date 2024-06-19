from db import db
from sqlalchemy import DateTime


class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.Date)
    user_type = db.Column(db.Integer, db.ForeignKey("user_types.user_type"))
    person_type = db.relationship("UserType", lazy="dynamic")
    password = db.Column(db.String(), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.Date, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)
    temporary_block = db.Column(DateTime, nullable=True)
