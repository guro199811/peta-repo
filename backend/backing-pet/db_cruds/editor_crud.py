from db import db
from models import Person


# Single editor cruds
def get_editor_by_person_id(person_id):
    '''Query the editor by person ID'''
    return db.session.execute(
        db.select(Person).where(Person.id == person_id, Person.user_type == 4)
    ).scalar()

# Multiple editor cruds
def get_all_editors():
    '''Retrieve all editors from the database.'''
    return db.session.execute(
        db.select(Person).where(Person.user_type == 4)
    ).scalars().all()