from website import db
from website.models import Type, Speciality, Pet_species, Pet_breed
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os


try:
    database_url = os.environ.get('DATABASE_URL1')
except:
    database_url = None


if database_url == None:
    engine = create_engine("postgresql://postgres:postgres@postgres:5432/petsite")
else:
    engine = create_engine(database_url)
    
session = Session(engine)
    
try:
    type_fixture = [
        (1, 'User'),
        (2, 'Admin'),
        (3, 'Vet'),
        (4, 'Editor')
    ]

    if not session.query(Type).first():
        for type_ in type_fixture:
            t = Type(type=type_[0], explanation=type_[1])  
            session.add(t)
        session.commit()

    specialities_fixture = [
        ('Cardiology', 'Speciality in heart conditions'),
        ('Dermatology', 'Speciality in skin disorders'),
        ('Ophthalmology', 'Speciality in eye diseases'),
        ('Orthopedics', 'Speciality in musculoskeletal system'),
        ('Neurology', 'Speciality in nervous system disorders'),
        ('Oncology', 'Speciality in cancer treatment'),
        ('Radiology', 'Speciality in medical imaging'),
        ('Surgery', 'Speciality in surgical procedures'),
        ('Internal Medicine', 'Speciality in internal diseases'),
        ('Behavioral Medicine', 'Speciality in behavioral disorders')
    ]

    if not session.query(Speciality).first():
        for spec in specialities_fixture:
            s = Speciality(specialty=spec[0], description=spec[1])
            session.add(s)
        session.commit()

    pet_species_fixture = [
        (1, 'Dog'),
        (2, 'Cat'),
        (3, 'Bird'),
        (4, 'Fish'),
        (5, 'Reptile'),
        (6, 'Small mammal'),
        (100, 'Other pet species')
    ]

    if not session.query(Pet_species).first():
        for pet_species in pet_species_fixture:
            p = Pet_species(species_id = pet_species[0], species = pet_species[1])
            session.add(p)
        session.commit()

    pet_breeds_fixture = [
        #Dogs
        (1, 'German Shepherd'),
        (1, 'Labrador Retriever'),
        (1, 'Golden Retriever'),
        (1, 'Bulldog'),
        (1, 'Beagle'),
        (1, 'Poodle'),
        (1, 'Rottweiler'),
        (1, 'Yorkshire Terrier'),
        (1, 'Boxer'),
        (1, 'Dachshund'),
        #Cats
        (2, 'Persian'),
        (2, 'Maine Coon'),
        (2, 'Siamese'),
        (2, 'British Shorthair'),
        (2, 'Bengal'),
        (2, 'Ragdoll'),
        (2, 'Sphynx'),
        (2, 'Scottish Fold'),
        (2, 'Russian Blue'),
        (2, 'Abyssinian'),
        #Birds
        (3, 'Parakeet'),
        (3, 'Canary'),
        (3, 'Cockatiel'),
        (3, 'African Grey Parrot'),
        (3, 'Budgerigar'),
        (3, 'Cockatoo'),
        (3, 'Lovebird'),
        (3, 'Finch'),
        (3, 'Macaw'),
        (3, 'Conure'),
        #Fish
        (4, 'Goldfish'),
        (4, 'Betta Fish'),
        (4, 'Guppy'),
        (4, 'Angelfish'),
        (4, 'Molly'),
        #Reptile
        (5, 'Green Iguana'),
        (5, 'Red-Eared Slider Turtle'),
        (5, 'Corn Snake'),
        (5, 'Leopard Gecko'),
        (5, 'Ball Python'),
        #Small Mammals
        (6, 'Hamster'),
        (6, 'Guinea Pig'),
        (6, 'Rabbit'),
        (6, 'Ferret'),
        (6, 'Chinchilla'),
       ]

    if not session.query(Pet_breed).first():
        for pet_breeds in pet_breeds_fixture:
            p = Pet_breed(species_id = pet_breeds[0], breed = pet_breeds[1])
            session.add(p)
        session.commit()


except Exception as e:
    print(f"An exception occurred: {str(e)}")
finally:
    session.close()
