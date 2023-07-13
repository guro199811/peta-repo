from flask import Blueprint, render_template, flash
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
    action = None
    return render_template("login/owner.html", user=current_user, action = action)

@views.route('/staff')
@login_required
def staff():
    action = None
    return render_template("login/staff.html", user=current_user, action = action)

@views.route('/vet')
@login_required
def vet():
    action = None
    return render_template("login/vet.html", user=current_user, action = action)

