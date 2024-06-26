from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user
from flask import jsonify
from models import UserType
from validators.user_type_schema import UserTypeSchema
from logs import logger_config

logger = logger_config.logger

blp = Blueprint("User Types", __name__, description="User Types operations")


@blp.route("/all/user_types")
class UserTypes(MethodView):
    def get(self):
        user_types = UserType.query.all()
        if not user_types:
            abort(404, message="No user types found")
        return jsonify([user_type.to_dict() for user_type in user_types])


@blp.route("/whoami")
class WhoAmI(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, UserTypeSchema)
    def get(self):
        return jsonify(
            f"{current_user.name} you are -> {current_user.person_type.desc}"
        )
