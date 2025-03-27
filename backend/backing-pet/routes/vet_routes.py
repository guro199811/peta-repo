from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Vet, Visit, Clinic, PersonClinic
from validators.visit_schema import VisitSchema, VisitAddSchema
from validators.clinic_schema import ClinicSchema, PersonToClinicSchema

from db_cruds.vet_crud import get_vet_by_person_id
from db_cruds.visit_crud import (
    get_visits_by_vet_id,
    get_all_visits_by_vet_and_person,
    get_visit_by_id,
)
from db_cruds.clinic_crud import (
    get_clinic_by_user_id,
    get_clinic_by_id,
    get_clinic_owner_by_user_and_clinic_id,
)

from logs import logger_config

logger = logger_config.logger

blp = Blueprint("Vet", __name__, description="Vet operations", url_prefix="/vet")


@blp.route("/visit")
class AddVisit(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, VisitSchema)
    def get(self):
        vet_data = get_vet_by_person_id(current_user.id)
        visits = get_visits_by_vet_id(vet_id=vet_data.vet_id)
        if not visits:
            abort(404, message="No visits found")
        return jsonify([visit.to_dict() for visit in visits])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(VisitAddSchema)
    @blp.response(200, VisitSchema)
    def post(self, visit_data):
        vet_data = get_vet_by_person_id(current_user.id)
        new_visit = Visit(vet_id=vet_data.vet_id, **visit_data)
        try:
            db.session.add(new_visit)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(new_visit.to_dict())


@blp.route("/visit/<int:person_id>")
class VetVisitsByPerson(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, VisitSchema)
    def get(self, person_id):
        vet_data = get_vet_by_person_id(current_user.id)
        if not vet_data:
            abort(404, message="Caller is not Veterinarian")
        visits = get_all_visits_by_vet_and_person(vet_data.vet_id, person_id)
        if not visits:
            abort(404, message=f"No visits found for person with id {person_id}")
        return jsonify([visit.to_dict() for visit in visits])


@blp.route("/visit/<int:visit_id>")
class VisitEditRoute(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, VisitSchema)
    def get(self, visit_id):
        visit = get_visit_by_id(visit_id=visit_id)
        if not visit:
            abort(404, message="Visit not found")
        if visit.vet_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This visit is not registered on " "this logged-in User.",
            )
        return jsonify(visit.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(VisitSchema)
    @blp.response(200, VisitSchema)
    def put(self, visit_data, visit_id):
        visit = get_visit_by_id(visit_id=visit_id)
        if not visit:
            abort(404, message="Visit not found")
        if visit.vet_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This visit is not registered on " "this logged-in User.",
            )
        for key, value in visit_data.items():
            if value is None:
                continue
            setattr(visit, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(visit.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, visit_id):
        visit = get_visit_by_id(visit_id)
        if not visit:
            abort(404, message="Visit not found")
        if visit.vet_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This visit is not registered on " "this logged-in User.",
            )
        try:
            db.session.delete(visit)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(visit.to_dict())


@blp.route("/clinic")
class ClinicRoutes(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonToClinicSchema)
    def get(self):
        clinic = get_clinic_by_user_id(current_user.id)
        if not clinic:
            abort(404, message="No clinics found for logged in user")
        return jsonify([clinic_data.to_dict() for clinic_data in clinic])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ClinicSchema)
    @blp.response(200, ClinicSchema)
    def post(self, clinic_data):
        vet_data = get_vet_by_person_id(current_user.id)
        if not vet_data:
            abort(404, message="Caller is not Veterinarian")
        if (
            not isinstance(clinic_data.get("coordinates"), str)
            or len(clinic_data.get("coordinates")) < 0
        ):
            abort(404, message="Invalid coordinates")
        clinic = Clinic(**clinic_data)
        try:
            db.session.add(clinic)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        try:
            clinic_person = PersonClinic(
                person_id=current_user.id,
                clinic_id=clinic.clinic_id,
                is_clinic_owner=True,
            )
            db.session.add(clinic_person)
            db.session.commit()
            # TODO: Add emailing for clinic creation confirmation...
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        clinic_data.update({"clinic_id": clinic.clinic_id})
        return jsonify(clinic_data)


@blp.route("/clinic/<int:clinic_id>")
class ClinicDetails(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, ClinicSchema)
    def get(self, clinic_id):
        clinic = get_clinic_by_id()
        if not clinic:
            abort(404, message="Clinic not found")
        return jsonify(clinic.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ClinicSchema)
    @blp.response(200, ClinicSchema)
    def put(self, clinic_data, clinic_id):
        vet_data = get_vet_by_person_id(current_user.id)
        if not vet_data or current_user.user_type != 2:
            abort(404, message="Caller is not a Vet nor an Admin")
        clinic = get_clinic_by_id(clinic_id)
        if not clinic:
            abort(404, message="Clinic not found")
        person_clinic = get_clinic_owner_by_user_and_clinic_id(
            current_user.id, clinic.clinic_id
        )
        if not person_clinic or current_user.user_type != 2:
            abort(
                400,
                message="User is not an clinic owner.",
            )
        for key, value in clinic_data.items():
            if value is None:
                continue
            setattr(clinic, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(clinic.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, clinic_id):
        vet_data = Vet.query.filter_by(person_id=current_user.id).first()
        if not vet_data or current_user.user_type != 2:
            abort(404, message="Caller is not a Vet nor an Admin")
        clinic = Clinic.query.filter_by(clinic_id=clinic_id).first()
        if not clinic:
            abort(404, message="Clinic not found")
        person_clinic = get_clinic_owner_by_user_and_clinic_id(
            current_user.id, clinic.clinic_id
        )
        if not person_clinic or current_user.user_type != 2:
            abort(400, message="User is not an clinic owner.")
        try:
            db.session.delete(clinic)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
