from flask import Blueprint, render_template, abort
from flask_login import (
    login_required,
    current_user)



views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("main.html")

@views.route('/owner')
@login_required
def owner():
    if current_user.type == 1:
        action = 0
        return render_template("login/owner.html", user=current_user, action = action)
    else:
        abort(404)

@views.route('/admin')
@login_required
def admin():
    if current_user.type == 2:        
        action = 0
        choice = 8
        return render_template("login/admin.html", user=current_user, action = action, choice = choice)
    else:
        abort(404)
@views.route('/vet')
@login_required
def vet():
    if current_user.type == 3:
        action = None
        return render_template("login/vet.html", user=current_user, action = action)
    else:
        abort(404)

@views.route('/editor')
@login_required
def editor():
    if current_user.type == 4:
        action = None
        return render_template("login/editor.html", user=current_user, action = action)
    else:
        abort(404)
