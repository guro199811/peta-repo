from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
import os
# import secrets
import logging


db = SQLAlchemy()
mail = Mail()

try:
    database_url = os.environ.get("DATABASE_URL1")
except Exception as e:
    logging.log(e)
    database_url = None


# Initialize Babel
babel = Babel()


def get_locale():
    # You can uncomment return for language testing purposes
    # return 'en'
    return request.args.get("lang") or \
        request.accept_languages.best_match(["ka", "en"])


def create_app(migrate):
    app = Flask(__name__, static_url_path="/static", static_folder="static")

    # Uncomment this for local developement,
    # for it sets security key with fixed value

    secret_key = 'shdiwkmalwdandwakjsndkwjanksjdnwkanskdwkajn'
    # And Comment this so it does not set random security key ##
    # secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key

    if database_url is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "postgresql://postgres:postgres@postgres:5432/petsite"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    # app.config['SERVER_NAME'] = 'localhost:8000'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    app.config.from_pyfile("mail_config.cfg")

    # Babel configuration setup

    app.config["BABEL_DEFAULT_LOCALE"] = "ka"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"

    # Initializing section
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)

    babel.init_app(app, locale_selector=get_locale)

    from .views import views
    from .auth import auth
    from .general_logic import general_logic
    from .ajax_logic import ajax_logic
    from .models import Person

    # Adding Blueprints for routing
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(general_logic, url_prefix="/")
    app.register_blueprint(ajax_logic, url_prefix="/")

    # Telling Flask how to load a user with primary key id,
    # loaded user will be accessed as Current_user in global and templates

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Person.query.get(int(id))

    return app
