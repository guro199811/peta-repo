from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Visit
from validators.visit_schema import VisitSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Visit", __name__, description="Visit operations", url_prefix="/visit"
)


@blp.route("/<int:visit_id>")
class VisitById(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, VisitSchema)
    def get(self, visit_id):
        visit = Visit.query.filter_by(visit_id=visit_id).first()
        if visit:
            return jsonify(visit.to_dict())
        abort(404, message="Visit not found")

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(VisitSchema)
    def put(self, visit_data, visit_id):
        visit = Visit.query.filter_by(visit_id=visit_id).first()
        if not visit:
            abort(404, message="Visit not found")
        if visit.vet_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This visit is not registered on "
                "this logged-in User."
            )
        for key, value in visit_data.items():
            if value is None:
                continue
            setattr(visit, key, value)
        try:
            db.session.add(visit)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(visit.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, visit_id):
        visit = Visit.query.filter_by(visit_id=visit_id).first()
        if not visit:
            abort(404, message="Visit not found")
        if visit.vet_id != current_user.id or current_user.user_type != 2:
            abort(
                400,
                message="This visit is not registered on "
                "this logged-in User."
            )
        try:
            db.session.delete(visit)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(visit.to_dict())


@blp.route("/by_pet/<int:pet_id>")
@jwt_required()
@blp.doc(security=[{"JWT Auth": []}])
@blp.response(200, VisitSchema)
def pet_visit(pet_id):
    visits = Visit.query.filter_by(pet_id=pet_id).all()
    if not visits:
        abort(404, message="No visits found")
    return jsonify([visit.to_dict() for visit in visits])


@blp.route("/by_vet/<int:vet_id>")
@jwt_required()
@blp.doc(security=[{"JWT Auth": []}])
@blp.response(200, VisitSchema)
def vet_visit(vet_id):
    visits = Visit.query.filter_by(vet_id=vet_id).all()
    if not visits:
        abort(404, message="No visits found")
    return jsonify([visit.to_dict() for visit in visits])


@blp.route("/by_clinic/<int:clinic_id>")
@jwt_required()
@blp.doc(security=[{"JWT Auth": []}])
@blp.response(200, VisitSchema)
def clinic_visit(clinic_id):
    visits = Visit.query.filter_by(clinic_id=clinic_id).all()
    if not visits:
        abort(404, message="No visits found")
    return jsonify([visit.to_dict() for visit in visits])
