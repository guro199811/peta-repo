from .tokens import generate_confirmation_token

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Person
from datetime import datetime
from datetime import date as dt

from flask_mail import Message

from flask_login import (
    login_user, 
    login_required, 
    logout_user, 
    current_user)

from flask import (
    Blueprint, 
    render_template, 
    request, flash, 
    redirect, url_for,
    current_app)


auth = Blueprint('auth', __name__)
#verimail = current_app.extensions['mail']

#შესვლის ფუნქცია, ამოწმებს მომხმარებელს ბაზაში
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('email')
        password = request.form.get('password')

        user = Person.query.filter_by(mail=mail).first()
        if user:
            if check_password_hash(user.password, password):
                #flash('წარმატება!', category='success')
                #flask_login-ს ვიყენებთ რომ დავიმახსოვროთ მომხმარებელი რომ შესულია
                login_user(user, remember=True)
                #ვიგებთ რა ტიპის მომხმარებელია
                type = user.type
                if type == 1:
                    return redirect(url_for('views.owner'))
                elif type == 2:
                    return redirect(url_for('views.admin'))
                elif type == 3:
                    return redirect(url_for('views.vet'))
                elif type == 4:
                    return redirect(url_for('views.editor'))
            else:
                flash('პაროლი არასწორია, გთხოვთ სცადოთ ხელახლა.', category='error')
        else:
            flash('ელ.ფოსტა არასწორედ წერია.', category='error')
    return render_template("login.html", user=current_user)


#გამოსვლის ფუნქცია
@auth.route('/logout')
@login_required
def logout():
    #დამახსოვრებული მომხმარებელი გამოდის
    logout_user()
    return redirect(url_for('auth.login'))


#რეგისტრაციის ფუნქცია
@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method =="POST":
        mail = request.form.get("email")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        password1 = request.form.get("password")
        password2 = request.form.get("repeat-password")
        phone = request.form.get("phone")
        address = request.form.get("address")
        choice = 1
        date = dt.today()

        #incade hes allready regisered
        user = Person.query.filter_by(mail=mail).first()

        if user:
            flash('ეს ელ.ფოსტა უკვე დარეგისტრირებულია.', category='error')
        elif len(mail) < 4:
            flash("ემაილი უნდა შეიცავდეს მინიმუმ 4 ასოს.", category="error")
        elif len(name) < 2:
            flash("სახელი უნდა იყოს მინიმუმ 1 ასოზე დიდი.", category="error")
        elif password1 != password2:
            flash("გამეორებული პაროლი არაა სწორი", category="error")
        elif len(password1) < 6:
            flash("პაროლის მინიმალური ზომა არის 6 სიმბოლო.", category="error")
        else:
            #Adding data to database
            new_user = Person(name=name, lastname=lastname, phone=phone,
                            mail=mail, address=address, created=date,
                            type=choice, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            token = generate_confirmation_token(new_user.mail, current_app)

            # Send a confirmation email
            confirmation_url = url_for('confirm_email', token=token, _external=True)
            message = Message('ელ.ფოსტის დასტური(Peta.ge)', recipients=[user.email])
            message.body = f'გთხოვთ დაადასტუროთ თქვენი ელ.ფოსტა მოცემული ბმულით: {confirmation_url}\n\n\nპატივისცემით, Peta-Team'
            mail.send(message)
            return redirect(url_for('views.verification'))

    return render_template("sign-up.html", user=current_user)