from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_


from . import db
from .models import *

general_logic = Blueprint('general_logic', __name__)



def register_pet(pet_name, pet_species, pet_breed, recent_vaccination, gender, birth_date):
    try:
        owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
        if owner is None:
            owner = Owner(person_id=current_user.id)
            db.session.add(owner)
            db.session.commit() 
        else:
            print(Owner.owner_id)
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


@general_logic.route('/<int:action>', methods=['GET', 'POST'])
@login_required
def owner_login(action):
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
                

        return render_template('login/owner.html', action=action)
    elif action == 2:
        # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
        owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
        if owner is None:
            try:
                result = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
                if result is None:
                    owner = Owner(person_id=current_user.id)
                    db.session.add(owner)
                    db.session.commit()
                else:
                    pass
            except:
                db.session.rollback()
                raise
        else:
            owner_id = owner.owner_id

            # მფლობელის იდენტიფიკატორით ცხოვლის მფლობლების მიღება
            pets = db.session.query(Pet).filter_by(owner_id=owner_id).order_by(Pet.pet_id.asc()).all()
            if len(pets) == 0:
                #flash('თქვენ ცხოველები არ გყავთ.')
                return render_template('login/owner.html', action=action, pets=None)
            else:
                return render_template('login/owner.html', action=action, pets=pets)
            # შაბლონის გამოტანა 'owner_login.html'-ში, action-ის მიხედვით
        

    elif action == 3:
        return render_template('login/owner.html', action=action)
    elif action == 4:
        Vets = Person.query.filter(or_(Person.type == 4, Person.type == 5)).all()
        return render_template('login/owner.html', action=action, vets = Vets)
    else:
        pass
            
@general_logic.route('/owner', methods=['GET', 'POST'])
@login_required
def change_user_data():
    changed = False
    if request.method =="POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        address = request.form.get('address')
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
        action = None
        if changed:
            flash('Changes saved successfully.', category='success')
    return render_template('login/owner.html', action = action)


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

            return redirect(url_for('general_logic.owner_login', action=action))

        #return render_template('owner.html', action=action, pet=pet, changed=changed)

    #flash('Pet not found.')
    return redirect(url_for('general_logic.owner_login', action=action))

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
        return redirect(url_for('general_logic.owner_login', action=2))
    else:
        flash("UNEXPECTED ERROR")
        return redirect(url_for('general_logic.owner_login', action=action))
