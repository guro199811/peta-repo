from db import db
from models import Person, Pet, PetSpecies


# Single pet crud
def get_pet_by_id(id):
    """Query the pet by ID"""
    return db.session.execute(db.select(Pet).where(Pet.pet_id == id)).scalar()


def register_pet(user_id: int, pet_data: dict):
    if pet_data.get("owner_id", None):
        owner_id = pet_data.pop("owner_id")
    else:
        owner_id = user_id
    new_pet = Pet(owner_id=owner_id, **pet_data)
    db.session.add(new_pet)
    db.session.commit()
    return new_pet


# Multiple pet crud
def get_all_pets():
    """Retrieve all pets from the database."""
    return db.session.execute(db.select(Pet)).scalars().all()


# TODO: Maybe implement pagination later on
def get_pets_by_owner_id(owner_id: int):
    return (
        db.session.execute(
            db.select(Pet).where(Pet.owner_id == owner_id).order_by(Pet.pet_id)
        )
        .scalars()
        .all()
    )
