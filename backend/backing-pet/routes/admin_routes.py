from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Person, Clinic, Visit, Vet
from validators.person_schema import (
    PersonGetterSchema,
    PersonUpdateSchema,
    AdminSpecificUpdateSchema,
)
from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Admin", __name__, description="Admin operations", url_prefix="/admin"
)


@blp.route("/person/<int:person_id>")
class PersonExtendedRoutes(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self, person_id):
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person not found")
        return jsonify(person.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PersonUpdateSchema)
    @blp.response(200, PersonGetterSchema)
    def put(self, user_data, person_id):
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person not found")
        for key, value in user_data.items():
            if value is None:
                continue
            setattr(person, key, value)
        try:
            db.session.commit()
            return {"message": f"successfully edited user {person.id} data"}
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(
                500,
                message="While editing user data, "
                + "unexpected error occured",
            )


@blp.route("/user_type/<int:person_id>")
class ChangeUserType(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def get(self, person_id):
        person = Person.query.get_or_404(person_id)
        return {f"person {person.id}": person.user_type}

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(AdminSpecificUpdateSchema)
    def put(self, request, person_id):
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person not found")
        if person.user_type == request["user_type"]:
            abort(
                400,
                message=f"Person {person.id} is already "
                + f"of type {request['user_type']}",
            )
        person.user_type = request["user_type"]
        if request["user_type"] == 3:
            new_vet = Vet(person_id=person.id)
            db.session.add(new_vet)
        if person.user_type == 3 and request["user_type"] != 3:
            vet = Vet.query.get_or_404(person_id=person.id)
            vet.active = False
        try:
            db.session.commit()
            return {f"Person id:{person.id}": person.user_type}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(
                500,
                message="While changing user type, "
                + "unexpected error occured",
            )


@blp.route("/all/users")
class AllUsers(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        users = Person.query.all()
        if bool(users) is False:
            abort(404, "No users found")
        spot_caller = [
            admin.to_dict() for admin in users if admin.id == current_user.id
        ]
        spot_caller.append("Caller")
        other_users = [
            user.to_dict() for user in users if user.id != current_user.id
        ]
        return jsonify(spot_caller + other_users)


@blp.route("/all/admins")
class AllAdmins(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        admins = Person.query.filter_by(user_type=2).all()
        if bool(admins) is False:
            spot_caller = [
                admin.to_dict()
                for admin in admins
                if admin.id == current_user.id
            ]
            spot_caller[0][current_user.id].update(caller=True)
            other_admins = [
                admin.to_dict()
                for admin in admins
                if admin.id != current_user.id
            ]
            return jsonify(spot_caller + other_admins)

        abort(404, "No admins found")


@blp.route("/all/vets")
class AllVets(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        vets = Vet.query.all()
        if bool(vets) is False:
            abort(404, "No vets found")
        return jsonify([vet.to_dict() for vet in vets])


@blp.route("/all/editors")
class AllEditors(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        editors = Person.query.all()
        if bool(editors) is False:
            return jsonify(
                [
                    editor.to_dict()
                    for editor in editors
                    if editor.user_type == 4
                ]
            )
        abort(404, "No editors found")


@blp.route("/all/clinics")
class AllClinics(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        clinics = Clinic.query.all()
        if bool(clinics) is False:
            return jsonify(
                [clinic.to_dict() for clinic in clinics if clinic.visiblity]
            )
        abort(404, "No clinics found")


@blp.route("/all/visits")
class AllVisits(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self):
        visits = Visit.query.all()
        if bool(visits) is False:
            return jsonify([visit.to_dict() for visit in visits])
        abort(404, "No visits found")
