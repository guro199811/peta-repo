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
    created = db.Column(db.Date)
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
    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    spec_id = db.Column(db.Integer, db.ForeignKey('specialities.spec_id'))
    speciality = db.relationship(Speciality)


class Pet_species(db.Model):
    __tablename__ = 'pet_species'
    species_id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))


class Pet_breed(db.Model):
    __tablename__ = 'pet_breeds'
    breed_id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('pet_species.species_id'))
    species = db.relationship(Pet_species)
    breed = db.Column(db.String(100))


class Pet(db.Model):
    __tablename__ = 'pets'
    pet_id = db.Column(db.Integer, primary_key=True)
    pet_species = db.Column(db.Integer, db.ForeignKey('pet_species.species_id'))
    species = db.relationship(Pet_species)
    pet_breed = db.Column(db.Integer, db.ForeignKey('pet_breeds.breed_id'))
    breed = db.relationship(Pet_breed)
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    recent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner = db.relationship(Owner)


class Admin(db.Model):
    __tablename__ = 'admins'
    active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


class Editor(db.Model):
    __tablename__ = 'editors'
    active = db.Column(db.Boolean, default=True)
    editor_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


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

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    posted = db.Column(db.DateTime)
    editor_id = db.Column(db.Integer, db.ForeignKey('editors.editor_id'))
    editor = db.relationship(Editor)




'''if __name__ == '__main__':
    app.run()
'''