from flask import Blueprint, render_template, abort
from flask_login import (
    login_required,
    current_user)
from functools import wraps

views = Blueprint('views', __name__)

action = 0

def grant_access(user_types):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.type in user_types:
                return view_func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator


@views.route('/')
def home():
    return render_template("main.html")

@views.route('/verification')
def verification():
    return render_template("login/admin.html", user=current_user, 
                           action = action)

@views.route('/owner')
@login_required
@grant_access([1])
def owner():
    return render_template("login/owner.html", user=current_user, 
                           action = action)

@views.route('/admin')
@login_required
@grant_access([2])
def admin():
    choice = 8
    return render_template("login/admin.html", user=current_user, 
                           action = action, choice = choice)

@views.route('/vet')
@login_required
@grant_access([3])
def vet():
    action = None
    return render_template("login/vet.html", user=current_user, 
                           action = action)

@views.route('/editor')
@login_required
@grant_access([4])
def editor():
    return render_template("login/editor.html", user=current_user, 
                           action = action)
