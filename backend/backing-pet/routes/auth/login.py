from datetime import datetime as dt
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

from db import db
from models import Person
from sqlalchemy.exc import SQLAlchemyError

from validators.person_schema import PlainPersonSchema
from validators.token_schema import TokenSchema

from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Login",
    __name__,
    description="User login operations",
    url_prefix="/auth",
)


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainPersonSchema)
    @blp.response(200, TokenSchema)
    def post(self, user_data):
        user = Person.query.filter_by(mail=user_data["mail"]).first()

        if not user or not pbkdf2_sha256.verify(
            user_data["password"], user.password
        ):
            abort(401, message="Invalid credentials")

        if user.temporary_block and dt.now() < user.temporary_block:
            abort(
                401,
                message="User has been temporarily "
                + f"blocked until {user.temporary_block}",
            )
        elif user.temporary_block and dt.now() >= user.temporary_block:
            try:
                user.temporary_block = None
                user.login_attempts = 0
                db.session.commit()
            except SQLAlchemyError as ex:
                db.session.rollback()
                logger.exception(
                    "Error occurred while updating user block status"
                )
                abort(500, message=f"Database Error: {ex}")

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        # TODO: Integrate Mailing confirmation
        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
