from db import db


class Vet(db.Model):
    __tablename__ = "vets"

    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person_data = db.relationship("Person", lazy="joined")
    has_license = db.Column(db.Boolean, default=False)
    temporary_license = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
                "vet_id": self.vet_id,
                "person_data": self.person_data.to_dict(),
                "has_license": self.has_license,
                "temporary_license": self.temporary_license,
                "active": self.active,
            }

    def __repr__(self):
        return f"{self.to_dict()}"
