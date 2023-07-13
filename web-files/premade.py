from website import db
from website.models import Type, Speciality
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://postgres:postgres@postgres:5432/petsite")
session = Session(engine)

try:
    type_fixture = [
        (1, 'Owner'),
        (2, 'Staff'),
        (4, 'Vet'),
        (3, 'Owner/Staff'),
        (5, 'Owner/Vet'),
        (6, 'Staff/Vet'),
        (7, 'Owner/Staff/Vet')
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
except Exception as e:
    print(f"An exception occurred: {str(e)}")
finally:
    session.close()
