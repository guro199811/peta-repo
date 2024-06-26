import os
from datetime import timedelta
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models  # noqa

from routes.token_routes import blp as TokenBlueprint
from routes.user_type_routes import blp as UserTypesBlueprint
from routes.home.home_page import blp as HomeBlueprint
from routes.auth.register import blp as RegisterBlueprint
from routes.auth.login import blp as LoginBlueprint
from routes.admin_routes import blp as AdminBlueprint
from routes.user_routes import blp as UserBlueprint
from routes.vet_routes import blp as VetBlueprint
from routes.pet_routes import blp as PetBlueprint
from routes.visit_routes import blp as VisitBlueprint


def create_app(db_url=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    #  --------------Flask Configurations------------------
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Pet Web Application API"
    app.config["API_VERSION"] = "Alpha 1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "JJSSGGDD"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    #  -------------Database Initialization-----------------
    db.init_app(app)
    #  -------------Flask_smorest (open-api)----------------
    api = Api(
        app,
        spec_kwargs={
            "components": {
                "securitySchemes": {
                    "JWT Auth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    }
                }
            }
        },
    )
    #  --------------Flask_jwt_extended---------------------
    jwt = JWTManager(app)  # noqa

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return models.Person.query.filter_by(id=jwt_data["sub"]).one_or_none()

    #  ---------------Managing Context----------------------
    with app.app_context():
        db.create_all()
    #  -----------------Blueprints--------------------------
    api.register_blueprint(TokenBlueprint)
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(RegisterBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(UserTypesBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(VetBlueprint)
    api.register_blueprint(PetBlueprint)
    api.register_blueprint(VisitBlueprint)

    #  -----------------------------------------------------
    return app
