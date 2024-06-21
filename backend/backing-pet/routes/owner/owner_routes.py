from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from db import db
from models import Person, PetOwner, Visit, Pet

from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Pets",
    __name__,
    description="Pet Owner operations",
    url_prefix="/owner"
)


@blp.route("/")
class OwnerRoutes(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def get(self):
        owner = Person.query.filter_by(id=current_user.id).first()
        if not owner:
            new_owner = PetOwner() 
        return {}