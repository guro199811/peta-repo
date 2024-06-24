from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Pet
from validators.pet_schema import PetSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint("Pets", __name__, description="Pet operations")


# TODO: This endpoint is intended to be used by the admin
# find way to enforce permissions
@blp.route("/all_pets")
class AllPets(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self):
        all_pets = db.session.query(Pet).all()
        if len(all_pets) > 0:
            pet_list = [pet.to_dict() for pet in all_pets]
            return jsonify(pet_list)
        abort(404, "No Pets found in database")


@blp.route("/pet/<int:pet_id>")
class PetOperations(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self, pet_id):
        pet = Pet.query.filter_by(pet_id=pet_id).first()
        if not pet:
            abort(404, message="Pet not found")
        return jsonify(pet.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PetSchema)
    def put(self, pet_data, pet_id):
        pet = Pet.query.filter_by(pet_id=pet_id).first()
        if not pet:
            abort(404, message="Pet not found")
        if pet.owner_id != current_user.id:
            abort(
                400,
                message="This pet is not registered on "
                "this logged-in User.",
            )
        # pet.pet_species = pet_data["pet_species"]
        # pet.pet_breed = pet_data["pet_breed"]
        # pet.gender = pet_data["gender"]
        # pet.medical_condition = pet_data["medical_condition"]
        # pet.current_treatment = pet_data["current_treatment"]
        # pet.recent_vaccination = pet_data["recent_vaccination"]
        # pet.name = pet_data["name"]
        # pet.birth_date = pet_data["birth_date"]
        pet.__dict__.update(pet_data)
        logger.debug("Updated pet: %s", pet)
        pet.owner_id = current_user.id
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            abort(500, message="Something went wrong")
        return {"message": f"Pet {pet.pet_id} Updated succesfully"}, 200

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, pet_id):
        pet = Pet.query.filter_by(id=pet_id).first()
        if not pet:
            abort(404, message="Pet not found")
        try:
            db.session.delete(pet)
            db.session.commit()
            return jsonify(pet.to_dict())
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            abort(500, message="Something went wrong")


@blp.route("/register_pet")
class RegisterPet(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PetSchema)
    @blp.response(200, PetSchema)
    def post(self, pet_data):
        new_pet = Pet(owner_id=current_user.id, **pet_data)
        try:
            db.session.add(new_pet)
            db.session.commit()
        except SQLAlchemyError:
            logger.exception("Could not register pet")
            abort(500, message="Something went wrong")
        return jsonify(new_pet.to_dict())


@blp.route("/pet_visits/<int:pet_id>")
class PetVisitOperations(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self, pet_id):
        """NOT IMPLEMENTED"""
        abort(500, message="Not Implemented")


@blp.route("/pet_history/<int:pet_id>")
class PetHistoryOperations(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PetSchema)
    def get(self, pet_id):
        """NOT IMPLEMENTED"""
        abort(500, message="Not Implemented")
