# Premade.py is Essential for Setting up database so it has values nessessery
# to Function correctly...

# We Are adding: phone_prefix, pet_breeds, pet_species ->  Premade data
import os

from models import UserType, PetSpecies, PetBreed, PhonePrefixes
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from logs import logger_config

logger = logger_config.logger

try:
    database_url = os.environ.get("DATABASE_URL")
    engine = create_engine(database_url)
    session = Session(engine)
except Exception:
    logger.exception("Database URL is not specified in enviroment variables.")


# This part of the code sets petbreeds to autoincrement (it was a bug earlier)
try:

    # Creating a sequence for breed_id
    sequence_command = text(
        """
    CREATE SEQUENCE pet_breeds_breed_id_seq;
    """
    )

    # Attaching the sequence to the breed_id column
    attach_sequence_command = text(
        "ALTER TABLE pet_breeds "
        + "ALTER COLUMN breed_id SET DEFAULT "
        + "nextval('pet_breeds_breed_id_seq'::regclass);"
    )

    if session.query(PetBreed).first():
        session.execute(sequence_command)
        session.execute(attach_sequence_command)
except Exception as e:
    logger.debug(e.__class__.__name__)


# Entering premade data is required for project to function correctly
try:
    type_fixture = [(1, "User"), (2, "Admin"), (3, "Vet"), (4, "Editor")]

    if not session.query(UserType).first():
        for type_ in type_fixture:
            t = UserType(user_type=type_[0], desc=type_[1])
            session.add(t)
        session.commit()

    prefix_fixture = [
        ("+995", 9, "🇬🇪"),  # Georgia
        ("+380", 9, "🇺🇦"),  # Ukraine
        ("+1", 10, "🇺🇸"),  # United States & Canada
        ("+44", 10, "🇬🇧"),  # United Kingdom
        ("+91", 10, "🇮🇳"),  # India
        ("+81", 10, "🇯🇵"),  # Japan
        ("+49", 10, "🇩🇪"),  # Germany
        ("+7", 10, "🇷🇺"),  # Russia
    ]
    if not session.query(PhonePrefixes).first():
        for prefix_ in prefix_fixture:
            p = PhonePrefixes(
                prefix=prefix_[0], nums=prefix_[1], icon=prefix_[2]
            )
            session.add(p)
        session.commit()

    pet_species_fixture = [
        (1, "Dog"),
        (2, "Cat"),
        (3, "Bird"),
        (4, "Fish"),
        (5, "Reptile"),
        (6, "Small mammal"),
        (100, "Other pet species"),
    ]

    if not session.query(PetSpecies).first():
        for pet_species in pet_species_fixture:
            p = PetSpecies(species_id=pet_species[0], species=pet_species[1])
            session.add(p)
        session.commit()

    pet_breeds_fixture = [
        # Dogs
        (1, "German Shepherd"),
        (1, "Labrador Retriever"),
        (1, "Golden Retriever"),
        (1, "Bulldog"),
        (1, "Beagle"),
        (1, "Poodle"),
        (1, "Rottweiler"),
        (1, "Yorkshire Terrier"),
        (1, "Boxer"),
        (1, "Dachshund"),
        (1, "Pitbull"),
        (1, "Other"),
        # Cats
        (2, "Persian"),
        (2, "Maine Coon"),
        (2, "Siamese"),
        (2, "British Shorthair"),
        (2, "Bengal"),
        (2, "Ragdoll"),
        (2, "Sphynx"),
        (2, "Scottish Fold"),
        (2, "Russian Blue"),
        (2, "Abyssinian"),
        (2, "Other"),
        # Birds
        (3, "Parakeet"),
        (3, "Canary"),
        (3, "Cockatiel"),
        (3, "African Grey Parrot"),
        (3, "Budgerigar"),
        (3, "Cockatoo"),
        (3, "Lovebird"),
        (3, "Finch"),
        (3, "Macaw"),
        (3, "Conure"),
        (3, "Other"),
        # Fish
        (4, "Goldfish"),
        (4, "Betta Fish"),
        (4, "Guppy"),
        (4, "Angelfish"),
        (4, "Molly"),
        (4, "Other"),
        # Reptile
        (5, "Green Iguana"),
        (5, "Red-Eared Slider Turtle"),
        (5, "Corn Snake"),
        (5, "Leopard Gecko"),
        (5, "Ball Python"),
        (5, "Other"),
        # Small Mammals
        (6, "Hamster"),
        (6, "Guinea Pig"),
        (6, "Rabbit"),
        (6, "Ferret"),
        (6, "Chinchilla"),
        (6, "Other"),
    ]

    if not session.query(PetBreed).first():
        for pet_breeds in pet_breeds_fixture:
            p = PetBreed(species_id=pet_breeds[0], breed=pet_breeds[1])
            session.add(p)
        session.commit()


except Exception:
    # Intentional Exception silencing
    logger.info(
        "Premade did not run... \
either data exists or Exception occured."
    )
finally:
    session.close()
