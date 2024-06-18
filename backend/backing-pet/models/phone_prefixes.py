from db import db


class PhonePrefixes(db.Model):
    __tablename__ = "phone_prefixes"
    prefix_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(10), unique=True)
    nums = db.Column(db.Integer)
    icon = db.Column(db.String(10), nullable=False, default="&#127987")
