from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Pet, Visit
from validators.person_schema import (
    PersonGetterSchema,
    PlainPersonUpdateSchema,
)
from validators.pet_schema import PetSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint("User", __name__, description="User operations")


@blp.route("/user_data")
class UserRoutes(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        """Retrieve the current user's data.

        This end-point retrieves the data of the currently logged-in user.
        It uses the `jwt_required` decorator to
        ensure that only authenticated users can access this endpoint.
        The retrieved data is then returned as a
        JSON response using the `jsonify` function.

        Parameters:
        None

        Returns:
        JSON response containing the current user's data."""
        return jsonify(current_user.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PlainPersonUpdateSchema)
    @blp.response(200, PlainPersonUpdateSchema)
    def put(self, user_data):
        """Edit the current user's data.

        This end-point edits the data of the currently logged-in user.
        It uses the `jwt_required` decorator to
        ensure that only authenticated users can access this endpoint.

        Parameters:
        None

        Returns:
        JSON response containing the edited user's data."""
        if not current_user:
            abort(401, message="Invalid credentials")
        current_user.name = user_data["name"]
        current_user.lastname = user_data["lastname"]
        current_user.phone = user_data["phone"]
        current_user.address = user_data["address"]
        try:
            db.session.commit()
            return {"message": "successfully edited user data", **user_data}
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(
                500,
                message="While editing user data, "
                + "unexpected error occured",
            )


@blp.route("/user_pets")
class UserPetOperations(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self):
        """
        Retrieve the list of pets owned by the current user.

        This method retrieves the list of pets owned by the currently
        logged-in user.
        It uses the `jwt_required` decorator to ensure that only
        authenticated users can access this endpoint.
        If no pets are found for the user, it returns a 404 Not
        Found status with an appropriate message.

        Parameters:
        None

        Returns:
        JSON response containing a list of dictionaries, each representing
        a pet owned by the user.
        Each dictionary contains the pet's data.

        If no pets are found, it Returns -> No pets found.
        """
        pets = Pet.query.filter_by(owner_id=current_user.id).all()
        if not pets:
            abort(404, message="No pets found")
        return jsonify([pet.to_dict() for pet in pets])


@blp.route("/user_visits")
class UserVisitOperations(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self):
        """
        Retrieve the list of visits made by the current user.

        This method retrieves the list of visits made by the currently
        logged-in user.
        It uses the `jwt_required` decorator to ensure that only
        authenticated users can access this endpoint.
        If no visits are found for the user, it returns a 404 Not
        Found status with an appropriate message.

        Parameters:
        None

        Returns:
        JSON response containing a list of dictionaries, each representing
        a visit made by the user.
        Each dictionary contains the visit's data.

        If no visits are found, it Returns -> No visits found.
        """
        visits = Visit.query.filter_by(owner_id=current_user.id).all()
        if not visits:
            abort(404, message="No visits found")
        return jsonify([visit.to_dict() for visit in visits])
