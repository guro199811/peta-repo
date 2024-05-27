# Database Models are being defined here

from flask_login import UserMixin
from sqlalchemy import DateTime

from . import db


class Type(db.Model):
    __tablename__ = "types"
    user_type = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))


class Person(db.Model, UserMixin):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.Date)
    user_type = db.Column(db.Integer, db.ForeignKey("types.user_type"))
    person_type = db.relationship(Type)
    password = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.Date, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)
    temporary_block = db.Column(DateTime, nullable=True)


class Owner(db.Model):
    __tablename__ = "owners"
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)


class Clinic(db.Model):
    __tablename__ = "clinics"
    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_name = db.Column(db.String(200))
    desc = db.Column(db.String(201))
    coordinates = db.Column(db.String(75))
    visibility = db.Column(db.Boolean, default=True)


class Vet(db.Model):
    __tablename__ = "vets"
    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    has_license = db.Column(db.Boolean, default=False)
    temporary_license = db.Column(db.Boolean, default=False)


class PersonToClinic(db.Model):
    __tablename__ = "bridges"
    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship(Clinic)
    is_clinic_owner = db.Column(db.Boolean, default=False)


class PetSpecies(db.Model):
    __tablename__ = "pet_species"
    species_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species = db.Column(db.String(50))


class PetBreed(db.Model):
    __tablename__ = "pet_breeds"
    breed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species_id = db.Column(db.Integer, db.ForeignKey("pet_species.species_id"))
    species = db.relationship(PetSpecies)
    breed = db.Column(db.String(100))


class Pet(db.Model):
    __tablename__ = "pets"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_species = db.Column(db.Integer, db.ForeignKey(
        "pet_species.species_id"))
    species = db.relationship(PetSpecies)
    pet_breed = db.Column(db.Integer, db.ForeignKey("pet_breeds.breed_id"))
    breed = db.relationship(PetBreed)
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    recent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship(Owner)


class PetHistory(db.Model):
    __tablename__ = "pet_history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"),
                          nullable=True)
    clinic = db.relationship(Clinic)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    pet = db.relationship(Pet)
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))


class Admin(db.Model):
    __tablename__ = "admins"
    active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)


class Editor(db.Model):
    __tablename__ = "editors"
    active = db.Column(db.Boolean, default=True)
    editor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)


class Visit(db.Model):
    __tablename__ = "visits"
    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship(Clinic)
    vet_id = db.Column(db.Integer, db.ForeignKey("vets.vet_id"))
    vet = db.relationship(Vet)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    pet = db.relationship(Pet)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship(Owner)
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posted = db.Column(db.DateTime)
    editor_id = db.Column(db.Integer, db.ForeignKey("editors.editor_id"))
    editor = db.relationship(Editor)


class Note(db.Model):
    __tablename__ = "notes"
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    created = db.Column(db.Date)
    content = db.Column(db.String(500))


class Requests(db.Model):
    __tablename__ = "requests"
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_type = db.Column(db.String(20))
    requester_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    reciever_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    request_sent = db.Column(db.Date)
    comment = db.Column(db.String(100), nullable=True)
    ref = db.Column(db.Integer, nullable=True)

    requester = db.relationship(
        "Person", foreign_keys=[requester_id], backref="sent_requests"
    )

    reciever = db.relationship(
        "Person", foreign_keys=[reciever_id], backref="received_requests"
    )

    approved = db.Column(db.Boolean, default=False, nullable=True)


class PhonePrefixes(db.Model):
    __tablename__ = "phone_prefixes"
    prefix_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(10), unique=True)
    nums = db.Column(db.Integer)
    icon = db.Column(db.String(10), nullable=False, default="&#127987")
