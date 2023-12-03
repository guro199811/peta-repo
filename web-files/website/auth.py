#This py file is intended for authentification logic, as well as everything thats involved with it

from .tokens import generate_token, init_serializer
from itsdangerous import SignatureExpired
from sqlalchemy.exc import IntegrityError


from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import *
from datetime import datetime, timedelta, date as dt
import re

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
    redirect, url_for,
    session)

from .views import grant_access
import logging

from flask import current_app as app 
from flask_babel import _

auth = Blueprint('auth', __name__)


#LogIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'tries' not in session:
        session['tries'] = 0

    if request.method == 'POST':
        mail = request.form.get('email')
        password = request.form.get('password')
        
        user = Person.query.filter_by(mail=mail).first()
        if user:
            # Check if the account is currently blocked
            if user.temporary_block and datetime.utcnow() < user.temporary_block:
                flash(_('თქვენი აქაუნთი დროებით დაბლოკილია, გთხოვთ სცადოთ მოგვიანებით.'), 'error')
                return render_template('login.html', user=current_user, tries=session['tries'])

            # Unblock the account if the block duration has passed
            if user.temporary_block and datetime.utcnow() >= user.temporary_block:
                user.temporary_block = None
                user.login_attempts = 0
                db.session.commit()
            
            # Check password and handle login attempts
            if check_password_hash(user.password, password):
                # Reset login attempts on successful login
                user.login_attempts = 0
                session['tries'] = 0
                db.session.commit()
                login_user(user, remember=True)
                if user.confirmed:
                    #Guessing what type of user logged in
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
                    return render_template("auths/verification.html", user=current_user, verification_type = 0)
            else:
                # Increment login attempts
                
                user.login_attempts += 1
                db.session.commit()
                session['tries'] = user.login_attempts

                if user.login_attempts >= 10:
                    # Block the account for 30 minutes
                    user.temporary_block = datetime.utcnow() + timedelta(minutes=30)
                    db.session.commit()
                    flash(_('10 წარუმატებელი ცდის შედეგად, აქაუნთი დაბლოკილია 30 წუთით.'), category='error')
                else:
                    error_message = _('პაროლი არასწორია, გთხოვთ სცადოთ ხელახლა. ცდების რაოდენობა დარჩენილია = {tries}')
                    flash(error_message.format(tries=10 - session["tries"]), 'error')

                return render_template('login.html', user=current_user, tries=session['tries'])
        else:
            flash(_('ელ.ფოსტა არ არის დარეგისტრირებული, გთხოვთ სცადოთ ხელახლა.'), 'error')
    return render_template("login.html", user=current_user, tries=session['tries'])


#Logout
@auth.route('/logout')
@login_required
def logout():
    #Remembered user logs out here
    logout_user()
    return redirect(url_for('auth.login'))


# Registration Function
@auth.route("/register", methods=['GET', 'POST'])
def register():
    prefixes = db.session.query(Phone_Prefixes).all()
    all_prefixes = []
    for prefix in prefixes:
        p = {
            'prefix': prefix.prefix,  # Use dot notation instead of indexing
            'nums': prefix.nums,      # Same here, use dot notation
            'icon': prefix.icon
        }
        all_prefixes.append(p)

    if request.method =="POST":
        mail = request.form.get("email")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        password1 = request.form.get("password")
        password2 = request.form.get("repeat-password")
        prefix = request.form.get('country_code')
        phone = request.form.get("phone")
        address = request.form.get("address")
        choice = 1
        date = dt.today()

        #incade hes allready regisered
        user = Person.query.filter_by(mail=mail).first()

        if user:
            flash(_('მოცემული ელ.ფოსტა უკვე დარეგისტრირებულია.'), category='error')
        elif len(mail) < 4:
            flash(_("ემაილი უნდა შეიცავდეს მინიმუმ 4 სიმბოლოს."), category="error")
        elif len(name) < 2:
            flash(_("სახელი უნდა იყოს მინიმუმ 1 ასოზე დიდი."), category="error")
        elif password1 != password2:
            flash(_("გამეორებული პაროლი არაა სწორი"), category="error")
        elif len(password1) < 6:
            flash(_("პაროლის მინიმალური ზომა არის 6 სიმბოლო."), category="error")
        elif not re.search("[a-zA-Z]", password1):
            flash(_("თქვენი მაროლი უნდა შეიცავდეს მინიმუმ 1 ასოს"),category="error")
        elif not re.search("[0-9]", password1):
            flash(_('თქვენი პაროლი უნდა შეიცავდეს მინიმუმ 1 ციფრს'), category="error")
        else:
            #Combining phone data
            phone = prefix + phone
            logging.warning(phone)

            #Adding data to database
            new_user = Person(name=name, lastname=lastname, phone=phone,
                            mail=mail, address=address, created=date,
                            type=choice, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            

            
            send_confirmation(new_user)
            return render_template("auths/verification.html", user=current_user, verification_type = 0)
    return render_template("sign-up.html", user=current_user, prefixes=all_prefixes)

#####################
#Email Confirmations
#####################

# Send a confirmation email
@auth.route('/send_confirmation')
def send_confirmation(new_user = current_user):
    token = generate_token(new_user.mail, app, 'email-confirm')
    verimail = Mail(app)    


    message = Message(_('ელ.ფოსტის დასტური(Petaworld.com)'), sender='noreply@peta.ge', recipients=[new_user.mail])
    confirmation_url = url_for('auth.confirm_token', token=token, _external=True)
    m = _('გთხოვთ დაადასტუროთ თქვენი ელ.ფოსტა მოცემული ბმულით: {confirmation_url}\nგთხოვთ გაითვალისწინოთб, რომ თქვენი ბმული გაუქმდება გამოგზავნიდან 1 საათში\n\n\nპატივისცემით, Peta-Team')
    message.body = m.format(confirmation_url)
    verimail.send(message)
    return render_template("auths/verification.html", verification_type = 0)



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
    

##########################################
# Functions to send a password reset email
##########################################

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Person.query.filter_by(mail=email).first()

        if user:
            send_password_reset_email(user)
            success_message = _('პაროლის შეცვლის იმეილი გაიგზავნა თქვენს {user.mail} ელ.ფოსტაზე')
            flash(success_message.format(user.mail), category='success')
        else:
            flash(_('ეს ელ.ფოსტა არ არის დარეგისტრირებული'), category='error')

    return render_template("auths/forgot_password.html", user=current_user)



def send_password_reset_email(user):
    token = generate_token(user.mail, app, 'password-reset')
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    verimail = Mail(app) 

    message = Message(_('პაროლის შეცვლა (Petaworld.com)'), sender='noreply@peta.ge', recipients=[user.mail])
    m = 'პაროლის შეცვლის ლინკი: {reset_url}\nლინკი გაუქმდება გამოგზავნიდან 1 საათში.\n\n\nPeta-Team'
    message.body = m.format(reset_url)
    verimail.send(message)
    

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('repeat-password')
        if new_password != confirm_password:
            flash(_('პაროლები არ ემთხვევა'), category='error')
        elif len(new_password) < 6:
            flash(_('პაროლი უნდა შეიცავდეს მინიმუმ 6 სიმბოლოს'), category='error')
        elif not re.search("[a-zA-Z]", new_password):
            flash(_("თქვენი პაროლი უნდა შეიცავდეს მინიმუმ 1 ასოს"))
        elif not re.search("[0-9]", new_password):
            flash(_('თქვენი პაროლი უნდა შეიცავდეს მინიმუმ 1 ციფრს'))
        else:
            email = confirm_password_token(token)
            user = Person.query.filter_by(mail=email).first()

            if user:
                # Update the user's password
                user.password = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash(_('ლინკი არ არის სწორი'), category='error')

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
    

########################################
#Functions for Confirming Clinic removal
########################################


#sending clinic removal email
@login_required
@grant_access([2, 3])
@auth.route('/send_clinic_deletion/<int:clinic_id>')
def clinic_removal_email(clinic_id):
    user = current_user
    token = generate_token(user.mail, app, 'remove-clinic')
    remove_url = url_for('auth.confirm_clinic_removal', clinic_id = clinic_id , token=token, _external=True)
    r_mail = Mail(app) 

    #checking if user is owner of that clinic for different messege
    try:
        person = db.session.query(P_C_bridge).\
            filter_by(clinic_id = clinic_id, \
            person_id = current_user.id).one_or_none()
        clinic = db.session.query(Clinic).filter_by(clinic_id = clinic_id).one()
        if person.is_clinic_owner:
            message = Message(_('დასტური კლინიკის წაშლაზე (Petaworld.com)'), sender='noreply@peta.ge', recipients=[user.mail])
            m = 'მოგესალმებით, გთხოვთ წაიკითხოთ!\n\nთქვენ ხართ მოცემული კლინიკის "{clinic.clinic_name}" დამრეგისტრირებელი,\n\n\
                მოცემული კლინიკის წაშლით,ანუ ბმულზე გადასვლის შედეგად თქვენ დარწმუნებული ხართ რომ შლით:\n\n\
                    • ყველა კავშირს მოცემულ კლინიკასთან (აღდგენა შეუძლებელია)\n\
                    • ყველა ვიზიტს რომელიც მოცემულ კლინიკაშია დარეგისტრირებული (აღდგენა შეუძლებელია)\n\
                    • ყველა თანამშრომლების კავშირებს კლინიკასთან (აღდგენა შეუძლებელია)\n\n\n\
                      {remove_url}\nლინკი გაუქმდება გამოგზავნიდან 1 საათში.\n\n\nPeta-Team'
            message.body = m.format(clinic.clinic_name, remove_url)
        else:
            message = Message(_('დასტური კლინიკასთან კავშირის გაწყვეტაზე (Petaworld.com)'), sender='noreply@peta.ge', recipients=[user.mail])
            m = 'თუ დარწმუნებული ხართ რომ გნებავთ კავშირის გაწყვეტა კლინიკასთან სახელად "{clinic.clinic_name}", გადადით მოცემულ ბმულზე: {remove_url}\nლინკი გაუქმდება გამოგზავნიდან 1 საათში.\n\n\nPeta-Team'
            message.body = m.format(clinic.clinic_name, remove_url)
    except Exception as e:
        flash(_('შეცდომა'))
        logging.warning(e)

    r_mail.send(message)
    return render_template("auths/verification.html", verification_type = 1)
    


#confirming clinic removal token
@auth.route('r_clinic/<int:clinic_id>/<token>', methods=['GET', 'DELETE'])
@login_required
@grant_access([2, 3])
def confirm_clinic_removal(clinic_id, token, expiration=3600):
    if 'serializer' not in globals():
        serializer = None
    if serializer is None:
        serializer = init_serializer(app)
    try:
        email = serializer.loads(token, salt='remove-clinic', max_age=expiration)
        try:
            bridge = db.session.query(P_C_bridge).filter_by(clinic_id = clinic_id, person_id = current_user.id).one_or_none()
            if bridge:
                clinic = db.session.query(Clinic).filter_by(clinic_id = clinic_id).one_or_none()
                if clinic:
                    if bridge.is_clinic_owner == True:
                         
                        try:
                            visits = db.session.query(Visit).filter_by(clinic_id = clinic.clinic_id).all()
                            for visit in visits:
                                db.session.delete(visit)
                                db.session.commit()
                        except Exception as e:
                            logging.warning(e)


                        try:
                            all_bridges = db.session.query(P_C_bridge).filter_by(clinic_id = clinic_id).all()
                            for a in all_bridges:
                                db.session.delete(a)
                                db.session.commit()
                        except Exception as e:
                            logging.warning(e)


                        db.session.delete(bridge)
                        db.session.delete(clinic)
                        db.session.commit()
                        return redirect(url_for('general_logic.vet_logic', choice = 5, action = 1))
                    elif bridge.is_clinic_owner == False:
                        db.session.delete(bridge)
                        db.session.commit()
            
            return redirect(url_for('general_logic.vet_logic', choice = 5, action = 1))
        except Exception as e:
            logging.warning(e)
        return email
    except SignatureExpired:
        return render_template('auths/expired-token.html', user=current_user,
                                clinic_id = clinic_id, expiredType = 2)

