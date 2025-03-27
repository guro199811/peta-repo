from db import db
from models import PetSpecies



def get_all_species():
    '''Retrieve all pet species from the database.'''
    return db.session.execute(db.select(PetSpecies)).scalars().all()