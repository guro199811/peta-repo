from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required
from models import Visit
from validators.visit_schema import VisitSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Visit", __name__, description="Visit operations", url_prefix="/visit"
)


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
