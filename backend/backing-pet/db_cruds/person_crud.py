from db import db

from models import Person


# Single person cruds
def get_person_by_id(id):
    '''Query the person by ID'''
    return db.session.execute(
        db.select(Person).where(Person.id == id)
    ).scalar()


def get_person_by_mail(mail):
    '''Query the person by mail address'''
    return db.session.execute(
        db.select(Person).where(Person.mail == mail)
    ).scalar()


# Many person cruds
def get_all_people():
    '''Retrieve all people from the database.'''
    return db.session.execute(db.select(Person)).scalars().all()


def get_all_admins():
    '''Retrieve all admins from the database.'''
    return db.session.execute(
        db.select(Person).where(Person.user_type == 2)
    ).scalars().all()