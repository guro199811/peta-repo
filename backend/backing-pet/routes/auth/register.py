from datetime import datetime as dt

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

# from flask_jwt_extended import create_access_token
from models import Person, PhonePrefixes
from db import db
from sqlalchemy.exc import SQLAlchemyError

from logs import logger_config

logger = logger_config.logger


blp = Blueprint(
    "Person", __name__, description="Person operations", url_prefix="/auth"
)


@blp.route("/register")
class PersonRegistration(MethodView):
    def get(self):
        prefixes = db.session.query(PhonePrefixes).all()
        if len(prefixes) == 0:
            abort(404, message="Phone Prefixes not found")
        all_prefixes = []
        for prefix in prefixes:
            p = {
                "prefix": prefix.prefix,
                "nums": prefix.nums,
                "icon": prefix.icon,
            }
            all_prefixes.append(p)
        return {"prefixes": all_prefixes}, 200

    def post(self, user_data):
        if Person.query.filter(Person.mail == user_data["mail"]).first():
            abort(409, message="User with that email already exists.")
        if user_data["password"] != user_data["repeat-password"]:
            abort(400, message="Password do not match")
        try:
            phone = user_data["prefix"] + user_data["phone"]
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
        finally:
            db.session.close()
        return {"message": "User created successfully"}, 201
