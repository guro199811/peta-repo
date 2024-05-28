from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from functools import wraps
from . import db
from .models import Admin, Vet, Editor

views = Blueprint("views", __name__)

# Action and Choice variables are
# reusable variables that is being used for navigation
action = 0
choice = 8

# This Decorator is created for granting access to certain types of users
# 1.Regular user
# 2.Administrator
# 3.Vet
# 4.Editor


def grant_access(user_types):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.confirmed and current_user.user_type in user_types:
                return view_func(*args, **kwargs)
            elif current_user.confirmed is False:
                return render_template(
                    "auths/verification.html", user=current_user,
                    verification_type=0)
            else:
                abort(404)
        return wrapper
    return decorator


@views.route("/")
def home():
    return render_template("main.html")


@views.route("/owner")
@login_required
@grant_access([1])
def owner():
    return render_template(
        "login/owner.html", user=current_user, action=action)


@views.route("/admin")
@login_required
@grant_access([2])
def admin():
    check = Admin.get_admin(current_user.id)
    if check is None:
        new_admin = Admin(person_id=current_user.id)
        db.session.add(new_admin)
        db.session.commit()

    return render_template(
        "login/admin.html", user=current_user, action=action, choice=choice
    )


@views.route("/vet")
@login_required
@grant_access([3])
def vet():
    check = Vet.get_vet(current_user.id)
    if check is None:
        new_vet = Vet(person_id=current_user.id)
        db.session.add(new_vet)
        db.session.commit()
    action = None
    return render_template(
        "login/vet.html", user=current_user, action=action, choice=choice
    )


@views.route("/editor")
@login_required
@grant_access([4])
def editor():
    check = Editor.get_editor(current_user.id)
    if check is None:
        new_editor = Editor(person_id=current_user.id)
        db.session.add(new_editor)
        db.session.commit()
    return render_template(
        "login/editor.html", user=current_user, action=action)


@views.route("/verification")
def verification():
    return render_template(
        "login/owner.html", user=current_user, action=action)


@views.route("/expired-token")
def expired_token():
    return render_template(
        "login/owner.html", user=current_user, action=action)
