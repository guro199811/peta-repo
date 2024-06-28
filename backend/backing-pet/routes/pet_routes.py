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


@blp.route("/register_pet")
class RegisterPet(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PetSchema)
    @blp.response(200, PetSchema)
    def post(self, pet_data):
        if pet_data.get("owner_id"):
            owner_id = pet_data.pop("owner_id")
        else:
            owner_id = current_user.id
        new_pet = Pet(owner_id=owner_id, **pet_data)
        try:
            db.session.add(new_pet)
            db.session.commit()
        except SQLAlchemyError:
            logger.exception("Could not register pet")
            abort(500, message="Something went wrong")
        return jsonify(new_pet.to_dict())


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
        pet.owner_id = current_user.id
        for key, value in pet_data.items():
            if value is None:
                continue
            setattr(pet, key, value)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            abort(500, message="Something went wrong")
        return {"message": f"Pet {pet.name} Updated succesfully"}, 200

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, pet_id):
        pet = Pet.query.filter_by(id=pet_id).first()
        if not pet:
            abort(404, message="Pet not found")
        if pet.owner_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This pet is not registered on "
                "this logged-in User.",
            )
        try:
            db.session.delete(pet)
            db.session.commit()
            return jsonify(pet.to_dict())
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            abort(500, message="Something went wrong")