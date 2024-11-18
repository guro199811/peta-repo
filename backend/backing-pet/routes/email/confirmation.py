# from flask.views import MethodView
# from flask import jsonify
# from flask_smorest import Blueprint
# from .generate_tokens import generate_token
# from flask_jwt_extended import current_user
# from logs import logger_config
# from db import db
# from models import Person
# from flask import current_app as app
# from flask_mail import Message, Mail

# logger = logger_config.logger

# blp = Blueprint(
#     "Account Confirmation", __name__,
#     description="Email confirmations",
#     url_prefix="/confirmation"
# )


# @blp.route("/send/account")
# class AccountConfirmation(MethodView):
#     def post(self, email):
#         current_user = Person.query.filter_by(email).first()
#         token = generate_token(current_user.mail, app, "email-confirm")
#         mail_service = Mail(app)
#         message = Message((
#             "Please confirm your email account by this link: "
#         ))


# TODO: Finish this
        
# @auth.route("/send_confirmation")
# def send_confirmation(new_user=current_user):
#     token = generate_token(new_user.mail, app, "email-confirm")
#     verimail = Mail(app)

#     message = Message(
#         _("ელ.ფოსტის დასტური(Petaworld.com)"),
#         sender="noreply@peta.ge",
#         recipients=[new_user.mail],
#     )
#     confirmation_url = url_for(
#         "auth.confirm_token", token=token, _external=True
#     )
#     m = _(
#         "გთხოვთ დაადასტუროთ თქვენი ელ.ფოსტა მოცემული ბმულით:"
#         + f" {confirmation_url}\nგთხოვთ გაითვალისწინოთб, "
#         + "რომ თქვენი ბმული გაუქმდება გამოგზავნიდან 1 საათში\n\n\n"
#         + "პატივისცემით, Peta-Team"
#     )
#     message.body = m.format(confirmation_url)
#     verimail.send(message)
#     return render_template("auths/verification.html", verification_type=0)


# # Recieve a confirmation link


# @auth.route("/confirm_email/<token>")
# def confirm_token(token, expiration=3600):
#     if "serializer" not in globals():
#         serializer = None
#     if serializer is None:
#         serializer = init_serializer(app)
#     try:
#         serializer.loads(token, salt="email-confirm", max_age=expiration)
#         current_user.confirmed = True
#         current_user.confirmed_on = dt.today()
#         db.session.commit()
#         return redirect(url_for("views.owner"))
#     except SignatureExpired:
#         return render_template(
#             "auths/expired-token.html", user=current_user, expiredType=0
#         )


