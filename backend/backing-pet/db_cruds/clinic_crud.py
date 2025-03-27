from db import db
from models import Clinic, PersonClinic


# Single clinic crud
def get_clinic_by_id(clinic_id):
    """Query the clinic by ID"""
    return db.session.execute(db.select(Clinic).where(Clinic.id == clinic_id)).scalar()


def get_clinic_by_user_id(user_id, broad=True):
    """Query the clinic by user ID"""
    if broad:
        return db.session.execute(
            db.select(PersonClinic).where(PersonClinic.person_id == user_id)
        ).scalar()
    else:
        return db.session.execute(
            db.select(Clinic)
            .join(PersonClinic)
            .where(PersonClinic.person_id == user_id)
        ).scalar()


def get_clinic_owner_by_user_and_clinic_id(user_id, clinic_id):
    """Query the clinic by user ID and clinic ID"""
    return db.session.execute(
        db.select(Clinic)
        .join(PersonClinic)
        .where(
            PersonClinic.person_id == user_id,
            PersonClinic.clinic_id == clinic_id,
            is_clinic_owner=True,
        )
    ).scalar()


# Multiple clinic cruds
def get_all_clinics():
    """Retrieve all clinics from the database."""
    return db.session.execute(db.select(Clinic)).scalars().all()


def get_all_clinics_and_owners():
    """Retrieve all clinics with their owners from the database."""
    return (
        db.session.execute(
            db.select(PersonClinic).where(PersonClinic.is_clinic_owner == True)
        )
        .scalars()
        .all()
    )
