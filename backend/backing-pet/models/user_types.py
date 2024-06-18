from db import db


class UserType(db.Model):
    __tablename__ = "user_types"
    user_type = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))
