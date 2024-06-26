from db import db


class UserType(db.Model):
    __tablename__ = "user_types"
    user_type = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(50))

    def to_dict(self):
        return {
            "user_type": self.user_type,
            "desc": self.explanation,
        }
