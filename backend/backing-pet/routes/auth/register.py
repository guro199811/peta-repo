from datetime import datetime as dt

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from models import Person, PhonePrefixes
from db import db
from sqlalchemy.exc import SQLAlchemyError

from validators.person_schema import PersonRegistrationSchema

from logs import logger_config

logger = logger_config.logger


blp = Blueprint(
    "Registration",
    __name__,
    description="User registration operations",
    url_prefix="/auth",
)


@blp.route("/register")
class UserRegister(MethodView):
    def get(self):
        """
        User Registration endpoint.

        This method retrieves all phone prefixes from the
        database and returns them in a list of dictionaries.

        Parameters:
        None

        Returns:
        dict: A dictionary containing a list of phone prefixes.
        """
        # Query Phone Prefixes
        prefixes = db.session.query(PhonePrefixes).all()
        if len(prefixes) == 0:
            abort(500, message="Phone Prefixes not found")
        all_prefixes = []
        for prefix in prefixes:
            p = {
                "prefix": prefix.prefix,
                "nums": prefix.nums,
                "icon": prefix.icon,
            }
            all_prefixes.append(p)
        return {"prefixes": all_prefixes}

    @blp.arguments(PersonRegistrationSchema)
    def post(self, user_data):
        """
        Handles POST request for User Registration endpoint.

        Validates user input, checks for existing email, and creates
        a new user in the database.

        Parameters:
        user_data (Json): A Json containing user registration data.

        Returns:
        dict: A dictionary with a success message and HTTP status code 201.
        """
        prefixes = db.session.query(PhonePrefixes).all()
        if len(prefixes) == 0:
            abort(500, message="Phone Prefixes not found")
        phone_prefixes = []
        number_standards = {}
        for prefix in prefixes:
            phone_prefixes.append(prefix.prefix)
            number_standards[prefix.prefix] = prefix.nums

        if Person.query.filter(Person.mail == user_data["mail"]).first():
            abort(409, message="User with that email already exists.")
        if user_data["password"] != user_data["repeat_password"]:
            abort(400, message="Password do not match")
        if user_data["prefix"] not in phone_prefixes:
            abort(400, message="Invalid phone prefix")
        if (
            len(str(user_data["phone"]))
            != number_standards[user_data["prefix"]]
        ):
            abort(400, message="Invalid number")
        try:
            phone = user_data["prefix"] + str(user_data["phone"])
            new_user = Person(
                mail=user_data["mail"],
                name=user_data["name"],
                lastname=user_data["lastname"],
                phone=phone,
                address=user_data["address"],
                created=dt.today(),
                user_type=1,  # TODO: For now its hardcoded, Fix it later
                password=pbkdf2_sha256.hash(user_data["password"]),
            )
        except KeyError as ex:
            abort(400, f"{ex}")
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception("Error occured while creating user")
            abort(500, {"Database Error": f"{ex}"})
        except Exception:
            logger.exception("Error occured while generating JWT")
            abort(500)
        finally:
            db.session.close()
        return {"message": "User created successfully"}, 201
