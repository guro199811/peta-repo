from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Vet, Visit
from validators.visit_schema import VisitSchema, VisitAddSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Vet", __name__, description="Vet operations", url_prefix="/vet"
)


@blp.route("/visit")
class AddVisit(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, VisitSchema)
    def get(self):
        vet_data = Vet.query.filter_by(person_id=current_user.id).first()
        visits = Visit.query.filter_by(vet_id=vet_data.vet_id).all()
        if not visits:
            abort(404, message="No visits found")
        return jsonify([visit.to_dict() for visit in visits])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(VisitAddSchema)
    @blp.response(200, VisitSchema)
    def post(self, visit_data):
        vet_data = Vet.query.filter_by(person_id=current_user.id).first()
        new_visit = Visit(vet_id=vet_data.vet_id, **visit_data)
        try:
            db.session.add(new_visit)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message="Database error")
        return jsonify(new_visit.to_dict())
