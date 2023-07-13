from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


from . import db


class Type(db.Model):
    __tablename__ = 'types'
    type = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))


class Person(db.Model, UserMixin):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    type = db.Column(db.Integer, db.ForeignKey('types.type'))
    person_type = db.relationship(Type)
    password = db.Column(db.String(150), nullable=False)


class Owner(db.Model):
    __tablename__ = 'owners'
    owner_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


class Speciality(db.Model):
    __tablename__ = 'specialities'
    spec_id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(150))


class Vet(db.Model):
    __tablename__ = 'vets'
    vet_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    spec_id = db.Column(db.Integer, db.ForeignKey('specialities.spec_id'))
    speciality = db.relationship(Speciality)


class Pet(db.Model):
    __tablename__ = 'pets'
    pet_id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    recent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner = db.relationship(Owner)


class Staff(db.Model):
    __tablename__ = 'help_centre'
    staff_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    type = db.Column(db.Integer, db.ForeignKey('types.type'))


class Visit(db.Model):
    __tablename__ = 'visits'
    visit_id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.vet_id'))
    vet = db.relationship(Vet)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))
    pet = db.relationship(Pet)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner = db.relationship(Owner)
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)


'''if __name__ == '__main__':
    app.run()
'''