from db import db
from models import Visit, Pet


def get_all_visits():
    '''Retrieve all visits from the database.'''
    return db.session.execute(db.select(Visit)).scalars().all()

def get_visit_by_id(visit_id):
    '''Retrieve a visit by id from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.visit_id == visit_id)
    ).scalar()

def get_visits_by_vet_id(vet_id):
    '''Retrieve all visits for a specific vet from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.vet_id == vet_id)
    ).scalars().all()

def get_visits_by_clinic_id(clinic_id):
    '''Retrieve all visits for a specific clinic from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.clinic_id == clinic_id)
    ).scalars().all()

def get_visits_by_pet_id(pet_id):
    '''Retrieve all visits for a specific pet from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.pet_id == pet_id)
    ).scalars().all()

def get_all_visits_by_vet_and_person(vet_id, person_id):
    '''Retrieve all visits for a specific vet and person from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.vet_id == vet_id, Visit.person_id == person_id)
    ).scalars().all()

def get_all_user_visits(user_id: int):
    '''Retrieve all visits for a specific user from the database.'''
    return db.session.execute(
        db.select(Visit).where(Visit.owner_id == user_id)
    ).scalars().all()