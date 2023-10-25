from .tokens import generate_token, init_serializer
from itsdangerous import SignatureExpired

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Person
from datetime import datetime
from datetime import date as dt

from flask_mail import Message, Mail

from flask_login import (
    login_user, 
    login_required, 
    logout_user, 
    current_user)

from flask import (
    Blueprint, 
    render_template, 
    request, flash, 
    redirect, url_for)

from flask import current_app as app 

auth = Blueprint('auth', __name__)


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
                if user.confirmed:
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
                    return render_template("verification.html", user=current_user)
            else:
                flash('პაროლი არასწორია, გთხოვთ სცადოთ ხელახლა.', category='error')
        else:
            flash('ელ.ფოსტა არ არის დარეგისტრირებული, გთხოვთ სცადოთ ხელახლა.', category='error')
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
            flash("ემაილი უნდა შეიცავდეს მინიმუმ 4 სიმბოლოს.", category="error")
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
            

            
            send_confirmation(new_user)
            return render_template("auths/verification.html", user=current_user)
    return render_template("sign-up.html", user=current_user)


# Send a confirmation email
@auth.route('/send_confirmation')
def send_confirmation(new_user = current_user):
    import logging
    logging.warning("###############")
    logging.warning(f"{new_user.id}")
    token = generate_token(new_user.mail, app, 'email-confirm')
    verimail = Mail(app)    


    message = Message('ელ.ფოსტის დასტური(Petaworld.com)', sender='noreply@peta.ge', recipients=[new_user.mail])
    confirmation_url = url_for('auth.confirm_token', token=token, _external=True)
    message.body = f'გთხოვთ დაადასტუროთ თქვენი ელ.ფოსტა მოცემული ბმულით: {confirmation_url}\nგთხოვთ გაითვალისწინოთб, რომ თქვენი ბმული გაუქმდება გამოგზავნიდან 1 საათში\n\n\nპატივისცემით, Peta-Team'
    verimail.send(message)
    return render_template("auths/verification.html")



# Recieve a confirmation link

@auth.route('/confirm_email/<token>')
def confirm_token(token, expiration=3600):
    if 'serializer' not in globals():
        serializer = None
    if serializer is None:
        serializer = init_serializer(app)
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
        current_user.confirmed = True
        current_user.confirmed_on = dt.today()
        db.session.commit()
        return redirect(url_for('views.owner'))
    except SignatureExpired:
        return render_template('auths/expired-token.html', user=current_user, expiredType = 0)
    


#Forgot Password Section

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Person.query.filter_by(mail=email).first()

        if user:
            send_password_reset_email(user)
            flash(f'პაროლის შეცვლის იმეილი გაიგზავნა თქვენს {user.mail} ელ.ფოსტაზე', category='success')
        else:
            flash('ეს ელ.ფოსტა არ არის დარეგისტრირებული', category='error')

    return render_template("auths/forgot_password.html", user=current_user)


# Function to send a password reset email

def send_password_reset_email(user):
    token = generate_token(user.mail, app, 'password-reset')
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    verimail = Mail(app) 

    message = Message('პაროლის შეცვლა (Petaworld.com)', sender='noreply@peta.ge', recipients=[user.mail])
    message.body = f'პაროლის შეცვლის ლინკი: {reset_url}\nლინკი გაუქმდება გამოგზავნიდან 1 საათში.\n\n\nPeta-Team'
    verimail.send(message)
    

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        import logging
        new_password = request.form.get('password')
        confirm_password = request.form.get('repeat-password')
        logging.warning(f"{new_password} , {confirm_password}")
        if new_password != confirm_password:
            flash('პაროლები არ ემთხვევა', category='error')
        elif len(new_password) < 6:
            flash('პაროლი უნდა შეიცავდეს მინიმუმ 6 სიმბოლოს', category='error')
        else:
            email = confirm_password_token(token)
            user = Person.query.filter_by(mail=email).first()

            if user:
                # Update the user's password
                user.password = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash('ლინკი არ არის სწორი', category='error')

    return render_template("auths/reset_password.html", token=token, user=current_user)



def confirm_password_token(token, expiration=3600):
    if 'serializer' not in globals():
        serializer = None
    if serializer is None:
        serializer = init_serializer(app)
    try:
        email = serializer.loads(token, salt='password-reset', max_age=expiration)
        return email
    except SignatureExpired:
        return render_template('auths/expired-token.html', user=current_user, expiredType = 1)