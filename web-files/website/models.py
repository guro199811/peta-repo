# Database Models are being defined here

from flask_login import UserMixin
from sqlalchemy import DateTime, func, String, cast, or_
from sqlalchemy.orm import aliased

from . import db


class Type(db.Model):
    __tablename__ = "types"
    user_type = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))


class Person(db.Model, UserMixin):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.Date)
    user_type = db.Column(db.Integer, db.ForeignKey("types.user_type"))
    person_type = db.relationship(Type)
    password = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.Date, nullable=True)
    login_attempts = db.Column(db.Integer, default=0)
    temporary_block = db.Column(DateTime, nullable=True)

    @classmethod
    def get_all_users(cls) -> list:
        """
        This method retrieves all Person models from the database.

        Parameters:
        cls (class): The class reference to the Person model.

        Returns:
        list: A list of Person model instances.
        """
        return db.session.query(cls).all()

    @classmethod
    def search_users(cls, search_query: str):
        """
        This method is used to search for users based on various criteria.

        Parameters:
        search_query (str): The search query string. This can be a partial or
        full name, email, address, or phone number.

        Returns:
        list: A list of Person model instances that match the search criteria.

        Note:
        The search is case-insensitive and uses the 'LIKE' operator to
        match the search query with the user's details.
        """
        return (
            db.session.query(cls)
            .filter(
                or_(
                    func.lower(cls.name).like(search_query),
                    func.lower(cls.lastname).like(search_query),
                    func.lower(cls.mail).like(search_query),
                    func.lower(cls.address).like(search_query),
                    cast(cls.phone, String).like(search_query),
                )
            )
            .all()
        )


class Owner(db.Model):
    __tablename__ = "owners"
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)

    @classmethod
    def get_owner(cls, person_id: int):
        """
        Retrieves a single Owner instance based on the provided person_id.

        Parameters:
        cls (class): The class reference to the Owner model.
        person_id (int): The unique identifier of the Person for whom
        the Owner is being retrieved.

        Returns:
        Optional[Owner]: An Owner instance if found, otherwise None.

        Note:
        This method uses the SQLAlchemy ORM to query the database and
        retrieve the Owner instance.
        """
        return db.session.query(cls).filter_by(
            person_id=person_id
            ).one_or_none()

    @classmethod
    def get_all_owners(cls) -> list:
        """
        Retrieves all Owner instances along with their associated Person
        and the count of their pets.

        Returns:
        list: A list of tuples, where each tuple contains
        an Owner instance,a Person instance,
        and the count of pets owned by the respective owner.
        The tuples are grouped by Owner and Person.

        Note:
        -> This method uses SQLAlchemy ORM to query the database.
        It performs a join operation between the Owner,
        -> Person, and Pet tables. The outer join is used
        to include owners who do not have any pets.
        -> The result is grouped by Owner and Person, and
        the count of pets is calculated using the SQL function count().
        """
        return (
            db.session.query(cls, Person, func.count(Pet.pet_id))
            .join(Person, cls.person_id == Person.id)
            .outerjoin(Pet, cls.owner_id == Pet.owner_id)
            .group_by(cls, Person)
            .all()
        )


class Clinic(db.Model):
    __tablename__ = "clinics"
    clinic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_name = db.Column(db.String(200))
    desc = db.Column(db.String(201))
    coordinates = db.Column(db.String(75))
    visibility = db.Column(db.Boolean, default=True)

    @classmethod
    def get_all_visible_clinics(cls) -> list:
        """
        Retrieves all visible clinics from the database.

        Parameters:
        cls (class): The class reference to the Clinic model.

        Returns:
        list: A list of Clinic model instances
        that have visibility set to True.

        Note:
        This method uses SQLAlchemy ORM to query the database.
        It filters the Clinic instances based on the 'visibility' column,
        and returns all the visible clinics.
        """
        return (
            db.session.query(cls).filter_by(
                visibility=True
                ).all()
        )


class Vet(db.Model):
    __tablename__ = "vets"
    active = db.Column(db.Boolean, default=True)
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    has_license = db.Column(db.Boolean, default=False)
    temporary_license = db.Column(db.Boolean, default=False)

    @classmethod
    def get_all_vets(cls) -> list:
        """
        Retrieves all active Vet instances along with their associated Person.

        Parameters:
        cls (class): The class reference to the Vet model.

        Returns:
        list: A list of tuples, where each tuple contains a Vet instance
        and a Person instance. The tuples are filtered based on the 'active'
        column, and only include active Vets.

        Note:
        This method uses SQLAlchemy ORM to query the database.
        It performs a join operation between the Vet and Person tables.
        The result is filtered based on the 'active' column,
        and only active Vets are returned.
        """
        return (
            db.session.query(cls, Person)
            .join(Person, cls.person_id == Person.id)
            .filter(cls.active is True)
            .all()
            )


class PersonToClinic(db.Model):
    __tablename__ = "bridges"
    bridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship(Clinic)
    is_clinic_owner = db.Column(db.Boolean, default=False)


class PetSpecies(db.Model):
    __tablename__ = "pet_species"
    species_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    species = db.Column(db.String(50))

    @classmethod
    def get_all_species(cls) -> list:
        """
        Retrieves all PetSpecies instances from the database.

        Returns:
        list: A list of PetSpecies model instances.
        """
        return db.session.query(cls).all()


class PetBreed(db.Model):
    __tablename__ = "pet_breeds"
    breed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species_id = db.Column(db.Integer, db.ForeignKey("pet_species.species_id"))
    species = db.relationship(PetSpecies)
    breed = db.Column(db.String(100))


class Pet(db.Model):
    __tablename__ = "pets"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_species = db.Column(db.Integer, db.ForeignKey(
        "pet_species.species_id"))
    species = db.relationship(PetSpecies)
    pet_breed = db.Column(db.Integer, db.ForeignKey("pet_breeds.breed_id"))
    breed = db.relationship(PetBreed)
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    recent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship(Owner)

    @classmethod
    def get_pets(cls, owner_id: int):
        """
        Retrieves all Pet instances associated with a specific owner.

        Parameters:
        cls (class): The class reference to the Pet model.
        owner_id (int): The unique identifier of the Owner for whom
        the Pets are being retrieved.

        Returns:
        list: A list of Pet model instances that belong to the specified owner.
        """
        return db.session.query(cls).filter_by(owner_id=owner_id).all()

    @classmethod
    def get_pet_extended(cls, owner_id: int):
        """
        Retrieves all Pet instances associated with a specific owner,
        along with their species and breed.

        Parameters:
        cls (class): The class reference to the Pet model.
        owner_id (int): The unique identifier of the Owner
        for whom the Pets are being retrieved.

        Returns:
        list: A list of tuples, where each tuple contains
        a Pet instance, its associated PetSpecies,
        and PetBreed. The tuples are filtered based on the
        'owner_id' and ordered by 'pet_id' in ascending order.

        Note:
        This method uses SQLAlchemy ORM to query the database.
        It performs a join operation between the
        Pet, PetSpecies, and PetBreed tables. The result is
        filtered based on the 'owner_id' and ordered by 'pet_id'.
        """
        return (
            db.session.query(cls, PetSpecies, PetBreed)
            .join(PetSpecies, cls.pet_species == PetSpecies.species_id)
            .join(PetBreed, cls.pet_breed == PetBreed.breed_id)
            .filter(cls.owner_id == owner_id)
            .order_by(cls.pet_id.asc())
            .all()
            )


class PetHistory(db.Model):
    __tablename__ = "pet_history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"),
                          nullable=True)
    clinic = db.relationship(Clinic)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    pet = db.relationship(Pet)
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))

    @classmethod
    def get_history_by_owner(cls, owner_id: int) -> list:
        """
        Retrieves all PetHistory instances associated with a specific owner.

        Parameters:
        cls (class): The class reference to the PetHistory model.
        owner_id (int): The unique identifier of the Owner for whom
        the PetHistory instances are being retrieved.

        Returns:
        List[Tuple[PetHistory, Pet]]: A list of tuples,
        where each tuple contains a PetHistory instance and its
        associated Pet instance. The tuples are filtered
        based on the 'owner_id' of the Pet.

        Note:
        This method uses SQLAlchemy ORM to query the database.
        It performs a join operation between the PetHistory and Pet tables.
        The result is filtered based on the 'owner_id' of the Pet.
        """
        return (
            db.session.query(cls, Pet)
            .join(Pet, cls.pet_id == Pet.pet_id)
            .filter(Pet.owner_id == owner_id)
            .all()
        )

    @classmethod
    def get_history_by_hist_id(cls, history_id: int) -> list:
        """
        Retrieves a single PetHistory instance based
        on the provided history_id.

        Parameters:
        cls (class): The class reference to the PetHistory model.
        history_id (int): The unique identifier of the PetHistory
        instance to retrieve.

        Returns:
        A PetHistory instance if found, otherwise None.

        Note:
        This method uses the SQLAlchemy ORM to query the database
        and retrieve the PetHistory instance.
        """
        return (
            db.session.query(cls)
            .filter_by(history_id=history_id)
            .one_or_none()
            )


class Admin(db.Model):
    __tablename__ = "admins"
    active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)


class Editor(db.Model):
    __tablename__ = "editors"
    active = db.Column(db.Boolean, default=True)
    editor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)


class Visit(db.Model):
    """
    A Visit represents a pet visit to a clinic by a vet.
    It contains information about the clinic, vet, pet, owner,
    diagnosis, treatment, comment, and date of the visit.
    """
    __tablename__ = "visits"
    visit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    clinic = db.relationship(Clinic)
    vet_id = db.Column(db.Integer, db.ForeignKey("vets.vet_id"))
    vet = db.relationship(Vet)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.pet_id"))
    pet = db.relationship(Pet)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.owner_id"))
    owner = db.relationship(Owner)
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    comment = db.Column(db.String(500))
    date = db.Column(db.Date)

    @classmethod
    def get_visits(cls, person_id: int) -> list:
        """
        Retrieve all visits made by the owner with the given person_id.

        Args:
            person_id (int): The id of the owner (Person instance).

        Returns:
            list: A list of tuples, where each tuple contains a Visit instance,
            Clinic instance, Vet instance, Owner instance, Pet instance,
            vet's name and lastname, owner's name and lastname, and pet's name.
            The visits are filtered by the owner's person_id.
        """
        vet_person = aliased(Person)
        owner_person = aliased(Person)
        return (db.session.query(
                    cls,
                    Clinic,
                    Vet,
                    Owner,
                    Pet,
                    vet_person.name.label("vet_name"),
                    vet_person.lastname.label("vet_lastname"),
                    owner_person.name.label("owner_name"),
                    owner_person.lastname.label("owner_lastname"),
                    Pet.name.label("pet_name"),
                )
                .join(Clinic, Clinic.clinic_id == cls.clinic_id)
                .join(Vet, Vet.vet_id == cls.vet_id)
                .join(Owner, Owner.owner_id == cls.owner_id)
                .join(Pet, Pet.pet_id == cls.pet_id)
                .join(vet_person, vet_person.id == Vet.person_id)
                .join(owner_person, owner_person.id == Owner.person_id)
                .filter(Owner.person_id == person_id)
                .all())


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posted = db.Column(db.DateTime)
    editor_id = db.Column(db.Integer, db.ForeignKey("editors.editor_id"))
    editor = db.relationship(Editor)


class Note(db.Model):
    """
    A Note represents a note or a remark made by a person.
    It contains information about the person who made the note,
    the date when the note was created, and the content of the note.
    """
    __tablename__ = "notes"
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    person = db.relationship(Person)
    created = db.Column(db.Date)
    content = db.Column(db.String(500))

    @classmethod
    def get_admin_notes(cls, person_id):
        """
        Retrieve all notes made by a specific person.

        Args:
            person_id (int): The id of the person who made the notes.

        Returns:
            list: A list of Note instances made by the person with
            the given person_id.
        """
        return db.session.query(cls).filter_by(
            person_id=person_id).all()


class Requests(db.Model):
    __tablename__ = "requests"
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_type = db.Column(db.String(20))
    requester_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    reciever_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    request_sent = db.Column(db.Date)
    comment = db.Column(db.String(100), nullable=True)
    ref = db.Column(db.Integer, nullable=True)

    requester = db.relationship(
        "Person", foreign_keys=[requester_id], backref="sent_requests"
    )

    reciever = db.relationship(
        "Person", foreign_keys=[reciever_id], backref="received_requests"
    )

    approved = db.Column(db.Boolean, default=False, nullable=True)


class PhonePrefixes(db.Model):
    __tablename__ = "phone_prefixes"
    prefix_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prefix = db.Column(db.String(10), unique=True)
    nums = db.Column(db.Integer)
    icon = db.Column(db.String(10), nullable=False, default="&#127987")
