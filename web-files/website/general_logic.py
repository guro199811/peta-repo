from flask import (Blueprint, render_template,
                request, flash, redirect, url_for,
                jsonify, abort)
from flask_login import login_required, current_user
from sqlalchemy import join, select, or_, func
from sqlalchemy.orm import contains_eager


from . import db
from .models import *
import logging
import json

general_logic = Blueprint('general_logic', __name__)

#owner_logic


#user allowence decorator (does not work as intended)
'''
def allow_users(user_types):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            # check usertype here 
            if current_user.type in user_types:
                return fun(*args, **kwargs)
            else:
                raise PermissionError("Access not allowed for this user type.")
            
        return wrapper
    return decorator
'''



def register_pet(pet_name, pet_species, pet_breed, recent_vaccination, gender, birth_date):
    try:
        owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
        if owner is None:
            owner = Owner(person_id=current_user.id)
            db.session.add(owner)
            db.session.commit() 
        if owner is not None:
            owner = db.session.query(Owner).filter_by(person_id = current_user.id).one()
            pet = Pet(owner_id=owner.owner_id, name=pet_name,
                    species=pet_species, breed=pet_breed,
                    recent_vaccination=recent_vaccination if recent_vaccination else None,
                    gender = gender, birth_date = birth_date)
            db.session.add(pet)
            db.session.commit()
            return True
    except Exception as e:
        flash(f"{e}")





@general_logic.route('/owner/<int:action>', methods=['GET', 'POST'])
@login_required
def owner_logic(action):
        if current_user.type != 1:
            abort(404)
        if action == 0:
            if request.method =="POST":
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                address = request.form.get('address')
                changed = change_user_data(firstname, lastname, address)
                if changed:
                    flash('Changes saved successfully.', category='success')
                return render_template('login/owner.html', action = action)
        elif action == 1:
            if request.method =="POST":
                pet_name = request.form.get('pet_name')
                pet_species = request.form.get('pet_species')
                pet_breed = request.form.get('pet_breed')
                recent_vaccination = request.form.get('recent_vaccination')
                gender = request.form.get('gender')
                birth_date = request.form.get('bdate')

                confirmation = register_pet(pet_name, pet_species, pet_breed, 
                                            recent_vaccination, gender, birth_date)
                if confirmation:
                    flash('ცხოველი დარეგისტრირდა წარმატებით', category='success')
                    

            return render_template('login/owner.html', action=action)
        elif action == 2:
            # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
            owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
            if owner is None:
                return render_template('login/owner.html', action=action, pets=None)
            else:
                owner_id = owner.owner_id

                # მფლობელის იდენტიფიკატორით ცხოვლის მფლობლების მიღება
                pets = db.session.query(Pet).filter_by(owner_id=owner_id).order_by(Pet.pet_id.asc()).all()
                if len(pets) == 0:
                    #flash('თქვენ ცხოველები არ გყავთ.')
                    return render_template('login/owner.html', action=action, pets=None)
                else:
                    return render_template('login/owner.html', action=action, pets=pets)
                # შაბლონის გამოტანა 'owner_logic.html'-ში, action-ის მიხედვით
            

        elif action == 3:
            return render_template('login/owner.html', action=action)
        elif action == 4:
            vets = db.session.query(Vet).filter_by(type = 3).all()
            return render_template('login/owner.html', action=action, vets = vets)
        else:
            abort(404)
                


#admin_logic

@general_logic.route('/admin/<int:choice>/<int:action>', methods=['GET', 'POST'])
@login_required
def admin_logic(choice, action):
    if current_user.type != 2:
        abort(404)
    if choice == 1:
        if action == 1:
            if request.method =="POST":
                pet_name = request.form.get('pet_name')
                pet_species = request.form.get('pet_species')
                pet_breed = request.form.get('pet_breed')
                recent_vaccination = request.form.get('recent_vaccination')
                gender = request.form.get('gender')
                birth_date = request.form.get('bdate')

                confirmation = register_pet(pet_name, pet_species, pet_breed, 
                                            recent_vaccination, gender, birth_date)
                if confirmation:
                    flash('ცხოველი დარეგისტრირდა წარმატებით', category='success')
                else:
                    flash('თქვენი ცხოველი ვერ დარეგისტრირდა', category='error')    

            return render_template('login/admin.html',choice = choice, action=action)
        elif action == 2:
            # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
            owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
            if owner is None:
                return render_template('login/admin.html',choice = choice, action=action, pets=None)
            else:
                owner_id = owner.owner_id

                # მფლობელის იდენტიფიკატორით ცხოვლის მფლობლების მიღება
                pets = db.session.query(Pet).filter_by(owner_id=owner_id).order_by(Pet.pet_id.asc()).all()
                if len(pets) == 0:
                    #flash('თქვენ ცხოველები არ გყავთ.')
                    return render_template('login/admin.html',
                                           choice = choice ,action=action, pets=None)
                else:
                    return render_template('login/admin.html',
                                           choice = choice, action=action, pets=pets)
                
            

        elif action == 3:
            return render_template('login/admin.html',
                                   choice  = choice, action=action)
        elif action == 4:
            vets = db.session.query(Vet).filter_by(type = 3).all()
            return render_template('login/admin.html',
                                    choice = choice, action=action,
                                    vets = vets)
        else:
            return render_template('login/admin.html',
                                   choice = choice, action = None)
                

    if choice == 2:
        owner_count = db.session.query(Owner).count()
        vet_count = db.session.query(Vet).count()
        editor_count = db.session.query(Editor).count()
        visit_count = db.session.query(Visit).count()
        # Add counts for other user types as needed

        data = [
            ['Users', 'User count chart'],
            ['Owners', owner_count],
            ['Vets', vet_count],
            ['Editors', editor_count],
            ['Visits', visit_count]
            # Add other user types and their respective counts here
        ]
        return render_template('login/admin.html',
                                    choice = choice, action=action,
                                    data = data)

    if choice == 3:
        users = db.session.query(Owner, Person, func.count(Pet.pet_id)  # Adding the pet counter
        ).join(Person, Owner.person_id == Person.id). \
            outerjoin(Pet, Owner.owner_id == Pet.owner_id). \
            group_by(Owner, Person).all()
        
        return render_template('login/admin.html',
                               choice=choice,
                               action=action,
                               users=users) 
    if choice == 4:
        users = db.session.query(Vet, Person, func.count(Visit.visit_id)  # Adding the pet counter
        ).join(Person, Vet.person_id == Person.id). \
            outerjoin(Visit, Visit.vet_id == Vet.vet_id). \
            group_by(Vet, Person).all()
        
        return render_template('login/admin.html',
                               choice=choice,
                               action=action,
                               users=users) 
    if choice == 5:
        users = db.session.query(Editor, Person, func.count(Post.post_id)  # Adding the pet counter
        ).join(Person, Editor.person_id == Person.id). \
            outerjoin(Post, Post.editor_id == Editor.editor_id). \
            group_by(Editor, Person).all()

        return render_template('login/admin.html',
                               choice=choice,
                               action=action,
                               users=users) 
    if choice == 6:
        pass
    if choice == 7:
        pass
    if choice == 8:
        if request.method =="POST":
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            address = request.form.get('address')
            changed = change_user_data(firstname, lastname, address)
            if changed:
                flash('Changes saved successfully.', category='success')
            return render_template('login/admin.html',choice = choice, action = action)

    return render_template('login/admin.html', choice = choice)


def change_user_data(firstname, lastname, address):
    changed = False
    if firstname is not None:
        current_user.name = firstname
        db.session.commit()
        changed = True
        
    if lastname is not None:
        current_user.lastname = lastname
        db.session.commit()
        changed = True
        
    if address is not None:
        current_user.address = address
        db.session.commit()
        changed = True
        
    db.session.commit()
    return changed



@general_logic.route('/admin/edit_user/<int:person_id>', methods=['GET', 'POST'])
@login_required
def edit_user(person_id):
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        mail = request.form.get('mail')
        type = request.form.get('type')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        person = db.session.query(Person).filter_by(id = person_id).one()
        person.name = name
        person.lastname = lastname
        person.mail = mail
        person.type = type
        flash(f"{person.type}, {type}")
        person.address = address
        person.phone = phone
        if len(phone) == 9:
            db.session.commit()
        else:
            flash(f"the number {phone} is not equal to 9", category = 'error')
        return redirect(url_for('general_logic.admin_logic',choice = 3, action=0))
    


@general_logic.route('edit/<int:action>/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(action, pet_id):
    print(pet_id)
    pet = db.session.query(Pet).filter_by(pet_id = pet_id).one_or_none()
    changed = False
    if pet:
        print(pet.pet_id)
        if request.method == 'POST':
            name = request.form.get('name')
            #species = request.form.get('species')
            breed = request.form.get('breed')
            recent_vaccination = request.form.get('recent_vaccination')
            if name is not None and name != '':
                pet.name = name
                db.session.commit()
                changed = True
                
            '''if species is not None:
                pet.species = species
                db.session.commit()
                changed = True'''
                
            if breed is not None and breed != '':
                pet.breed = breed
                db.session.commit()
                changed = True

            if recent_vaccination is not None and recent_vaccination != '':
                pet.recent_vaccination = recent_vaccination
                db.session.commit()
                changed = True
            if changed:
                flash('მონაცემები წარმატებით შეიცვალა', category='success')
            if current_user.type == 1:
                return redirect(url_for('general_logic.owner_logic', action=action))
            elif current_user.type == 2:
                return redirect(url_for('general_logic.admin_logic',choice = 1, action=action))
                return 
        #return render_template('owner.html', action=action, pet=pet, changed=changed)

    #flash('Pet not found.')
    return redirect(url_for('general_logic.owner_logic', action=action))


@general_logic.route('delete/<int:action>/<int:pet_id>', methods=['GET', 'DELETE'])
@login_required
def remove_pet(action, pet_id):
    pet = db.session.query(Pet).filter_by(pet_id=pet_id).one_or_none()
    if pet is not None:
        owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
        if owner is not None:
            try:
                db.session.delete(pet)
                db.session.commit()
                
                remaining_pets = db.session.query(Pet).filter_by(owner_id=owner.owner_id).all()
                if not remaining_pets:
                    db.session.delete(owner)
                    db.session.commit()
                
            except Exception as e:
                flash(e)
        if current_user.type == 1:
            return redirect(url_for('general_logic.owner_logic', action=2))
        if current_user.type == 2:
            return redirect(url_for('general_logic.admin_logic',choice = 1, action=2))
    else:
        abort(404)
