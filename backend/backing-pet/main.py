import os

from flask import Flask
from flask_smorest import Api

from db import db
import models  # noqa: F401


def create_app(db_url=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    #  --------------Flask Configurations------------------
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
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
    #  -------------Database Initialization-----------------
    db.init_app(app)
    #  -------------Flask_smorest (open-api)----------------
    api = Api(app)  # noqa: F841
    #  ---------------Managing Context----------------------
    with app.app_context():
        db.create_all()
    #  -----------------Blueprints--------------------------
    #  -----------------------------------------------------
    return app
