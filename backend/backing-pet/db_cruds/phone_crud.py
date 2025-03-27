from db import db
from models import PhonePrefixes


def get_phone_prefixes() -> PhonePrefixes:
    '''Retrieve all phone prefixes from the database.'''
    return db.session.execute(db.select(PhonePrefixes)).scalars().all()