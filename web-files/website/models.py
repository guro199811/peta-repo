from flask_login import UserMixin


from . import db


class Type(db.Model):
    __tablename__ = 'types'
    type = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))


class Person(db.Model, UserMixin):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.Date)
    type = db.Column(db.Integer, db.ForeignKey('types.type'))
    person_type = db.relationship(Type)
    password = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.Date, nullable=True)


class Owner(db.Model):
    __tablename__ = 'owners'
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


class Speciality(db.Model):
    __tablename__ = 'specialities'
    spec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialty = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(150))


class Clinic(db.Model):
    __tablename__ = 'clinics'
    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_name = db.Column(db.String(200))
    desc = db.Column(db.String(201))
    coordinates = db.Column(db.String(75))


class Vet(db.Model):
    __tablename__ = 'vets'
    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    spec_id = db.Column(db.Integer, db.ForeignKey('specialities.spec_id'))
    speciality = db.relationship(Speciality)



class P_C_bridge(db.Model):
    __tablename__ = 'bridges'
    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.clinic_id'))
    clinic = db.relationship(Clinic)
    is_clinic_owner = db.Column(db.Boolean, default=False)
    


class Pet_species(db.Model):
    __tablename__ = 'pet_species'
    species_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species = db.Column(db.String(50))


class Pet_breed(db.Model):
    __tablename__ = 'pet_breeds'
    breed_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species_id = db.Column(db.Integer, db.ForeignKey('pet_species.species_id'))
    species = db.relationship(Pet_species)
    breed = db.Column(db.String(100))


class Pet(db.Model):
    __tablename__ = 'pets'
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    
    
class Pet_history(db.Model):
    __tablename__ = 'pet_history'
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))
    pet = db.relationship(Pet)
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))


class Admin(db.Model):
    __tablename__ = 'admins'
    active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


class Editor(db.Model):
    __tablename__ = 'editors'
    active = db.Column(db.Boolean, default=True)
    editor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)


class Visit(db.Model):
    __tablename__ = 'visits'
    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.clinic_id'))
    clinic = db.relationship(Clinic)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.vet_id'))
    vet = db.relationship(Vet)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))
    pet = db.relationship(Pet)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner = db.relationship(Owner)
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posted = db.Column(db.DateTime)
    editor_id = db.Column(db.Integer, db.ForeignKey('editors.editor_id'))
    editor = db.relationship(Editor)


class Note(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship(Person)
    created = db.Column(db.Date)
    content = db.Column(db.String(500))




'''if __name__ == '__main__':
    app.run()
'''
