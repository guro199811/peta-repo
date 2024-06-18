from flask.views import MethodView
from flask_smorest import Blueprint


blp = Blueprint("Home page", __name__,
                description="Home page operations")


@blp.route("/")
class HomePage(MethodView):
    def get(self):
        return {
            "welcome": "Welcome to our website!",
            "home_text": "Our website is created for your lovely" +
            " pet veterinary care needs."}
