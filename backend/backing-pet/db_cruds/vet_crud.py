from db import db
from models import Vet



# Single vet cruds
def get_vet_by_person_id(person_id):
    '''Query the vet by person ID'''
    return db.session.execute(
        db.select(Vet).where(Vet.person_id == person_id)
    ).scalar()


# Multiple vet cruds
def get_all_vets():
    '''Retrieve all vets from the database.'''
    return db.session.execute(db.select(Vet)).scalars().all()


def get_active_vets():
    '''Retrieve all active vets from the database.'''
    return db.session.execute(
        db.select(Vet).where(Vet.active == True)
    ).scalars().all()