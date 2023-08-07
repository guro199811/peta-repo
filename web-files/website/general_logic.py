from flask import (Blueprint, render_template,
                request, flash, redirect, url_for,
                jsonify, abort)
from flask_login import login_required, current_user
from sqlalchemy import join, select, or_, func, and_, cast, String
from sqlalchemy.orm import contains_eager, aliased
from sqlalchemy.orm.exc import NoResultFound
from datetime import date as dt, timedelta



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
            breed = db.session.query(Pet_breed).filter_by(breed = pet_breed).one()
            pet = Pet(owner_id=owner.owner_id, name=pet_name,
                    pet_species=pet_species, pet_breed=breed.breed_id,
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
            
                    

            return render_template('login/owner.html', action=action)
        if action == 1:
            # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
            owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
            if owner is None:
                return render_template('login/owner.html', action=action, pets=None)
            else:
                owner_id = owner.owner_id

                # მფლობელის იდენტიფიკატორით ცხოვლის მფლობლების მიღება
                pets = db.session.query(Pet, Pet_species, Pet_breed).\
                    join(Pet_species, Pet.pet_species == Pet_species.species_id).\
                    join(Pet_breed, Pet.pet_breed == Pet_breed.breed_id).\
                    filter(Pet.owner_id == owner_id).\
                    order_by(Pet.pet_id.asc()).\
                    all()
                if len(pets) == 0:
                    #flash('თქვენ ცხოველები არ გყავთ.')
                    return render_template('login/owner.html', action=action, pets=None)
                else:
                    return render_template('login/owner.html', action=action, pets=pets)
                # შაბლონის გამოტანა 'owner_logic.html'-ში, action-ის მიხედვით
            
        elif action == 2:
            owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
            if owner:
                pet_history = db.session.query(Pet_history, Pet).\
                    join(Pet, Pet_history.pet_id == Pet.pet_id).\
                    filter(Pet.owner_id == owner.owner_id).all()
                if request.method == "GET":
                    return render_template('login/owner.html',
                        action = action, 
                        pet_history = pet_history)
                elif request.method == "POST":
                    history_id = request.form.get('history_id')
                    treatment = request.form.get('treatment')
                    comment = request.form.get('comment')
                    date = request.form.get('date')
                    
                    history = db.session.query(Pet_history).filter_by(history_id = history_id).one_or_none()
                    if history:
                        if treatment:
                            history.treatment = treatment
                        if comment:
                            history.comment = comment
                        if date:
                            history.date = date
                    else:
                        abort(404)
                    db.session.commit()

                    return render_template('login/owner.html',
                                        action = action,
                                        pet_history = pet_history)
            else:
                return render_template('login/owner.html',
                                    action = action,
                                    pet_history = None)
        elif action == 3:
            return render_template('login/owner.html', action=action)
        
        elif action == 4:
            vets = db.session.query(Vet, Person).join(Person, Vet.person_id == Person.id).filter(Vet.active == True).all()
            return render_template('login/owner.html', action=action, vets = vets)
        
        elif action == 5:
            if request.method == "GET":
                pet_species_list = db.session.query(Pet_species).all()
                return render_template('login/owner.html', action = action, pet_species_list = pet_species_list)
            
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

            return render_template('login/owner.html', action=1)
        
        elif action == 6: #needs pets from current user
            if request.method == "GET":    
                owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
                if owner:
                    pets = db.session.query(Pet).filter_by(owner_id = owner.owner_id).all()
                    return render_template('login/owner.html',
                                    action = 6, pets = pets)
                else:
                    return render_template('login/owner.html',
                                    action = 6, pets = None)
            elif request.method == "POST":
                pet_id = request.form.get('pet_name')
                treatment = request.form.get('treatment')
                comment = request.form.get('comment')
                date = request.form.get('date')
                new_history = Pet_history(pet_id = pet_id, treatment = treatment,
                                        date = date, comment = comment)
                db.session.add(new_history)
                db.session.commit()
                return render_template('login/owner.html',
                                    action = 2)

        else:
            abort(404)
                


#admin_logic

@general_logic.route('/admin/<int:choice>/<int:action>', methods=['GET', 'POST'])
@login_required
def admin_logic(choice, action):
    if current_user.type != 2:
        abort(404)
    if choice == 0:
    # Handle search functionality here
        search_query = request.args.get('q')
        if search_query:
            # Perform a case-insensitive search on the 'persons' table
            search_query = f"%{search_query.lower()}%"
            search_results = db.session.query(Person).filter(
                or_(
                    func.lower(Person.name).like(search_query),
                    func.lower(Person.lastname).like(search_query),
                    func.lower(Person.mail).like(search_query),
                    func.lower(Person.address).like(search_query),
                    cast(Person.phone, String).like(search_query)
                )
            ).all()

        return render_template('login/admin.html', choice=choice, action = search_results)

    
    if choice == 1:
        if action == 1:
            # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
            owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
            if owner is None:
                return render_template('login/admin.html',choice = choice, action=action, pets=None)
            else:
                owner_id = owner.owner_id

                # მფლობელის იდენტიფიკატორით ცხოვლის მფლობლების მიღება
                pets = db.session.query(Pet, Pet_species, Pet_breed).\
                    join(Pet_species, Pet.pet_species == Pet_species.species_id).\
                    join(Pet_breed, Pet.pet_breed == Pet_breed.breed_id).\
                    filter(Pet.owner_id == owner_id).\
                    order_by(Pet.pet_id.asc()).\
                    all()
                if len(pets) == 0:
                    #flash('თქვენ ცხოველები არ გყავთ.')
                    return render_template('login/admin.html',
                                           choice = choice ,action=action, pets=None)
                else:
                    return render_template('login/admin.html',
                                           choice = choice, action=action, pets=pets)
                
        elif action == 2:
            owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
            if owner:
                pet_history = db.session.query(Pet_history, Pet).\
                    join(Pet, Pet_history.pet_id == Pet.pet_id).\
                    filter(Pet.owner_id == owner.owner_id).all()
                if request.method == "GET":
                    return render_template('login/admin.html',
                        choice = choice, action = action, 
                        pet_history = pet_history)
                elif request.method == "POST":
                    history_id = request.form.get('history_id')
                    treatment = request.form.get('treatment')
                    comment = request.form.get('comment')
                    date = request.form.get('date')
                    
                    history = db.session.query(Pet_history).filter_by(history_id = history_id).one_or_none()
                    if history:
                        if treatment:
                            history.treatment = treatment
                        if comment:
                            history.comment = comment
                        if date:
                            history.date = date
                    db.session.commit()

                    return render_template('login/admin.html',
                                    choice = choice, action = action,
                                    pet_history = pet_history)
            else:
                return render_template('login/admin.html',
                                    choice = choice, action = action,
                                    pet_history = None)

        
        elif action == 3:
            return render_template('login/admin.html',
                                   choice  = choice, action=action)
        
        elif action == 4:
            vets = db.session.query(Vet, Person).join(Person, Vet.person_id == Person.id).filter(Vet.active == True).all()
            return render_template('login/admin.html',
                                    choice = choice, action=action,
                                    vets = vets)
        
        elif action == 5:
            if request.method == "GET":
                pet_species_list = db.session.query(Pet_species).all()
                return render_template('login/admin.html', choice = choice, action = action, pet_species_list = pet_species_list)
            
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
        
        elif action == 6: #needs pets from current user
            if request.method == "GET":    
                owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
                if owner:
                    pets = db.session.query(Pet).filter_by(owner_id = owner.owner_id).all()
                    return render_template('login/admin.html',
                                    choice = choice, action = 6, pets = pets)
            elif request.method == "POST":
                pet_id = request.form.get('pet_name')
                treatment = request.form.get('treatment')
                comment = request.form.get('comment')
                date = request.form.get('date')
                new_history = Pet_history(pet_id = pet_id, treatment = treatment,
                                        date = date, comment = comment)
                db.session.add(new_history)
                db.session.commit()
                return redirect(url_for('login/admin.html', choice=choice, action=2))
        else:
            return render_template('login/admin.html', choice=1, action=None)
           

    if choice == 2:
        owner_count = db.session.query(Owner).count()
        vet_count = db.session.query(Vet).filter_by(active = True).count()
        editor_count = db.session.query(Editor).filter_by(active = True).count()
        admin_count = db.session.query(Admin).count()


        # Subquery to find the IDs of owners, vets, and editors
        owner_ids = db.session.query(Owner.person_id)
        vet_ids = db.session.query(Vet.person_id)
        editor_ids = db.session.query(Editor.person_id)

        other_users = db.session.query(Person).filter(
            and_(
                Person.id.notin_(owner_ids),
                Person.id.notin_(vet_ids),
                Person.id.notin_(editor_ids)
            )
        ).count()

        owners = db.session.query(
            Owner, Person, func.count(Pet.pet_id)
        ).join(Person, Owner.person_id == Person.id). \
        outerjoin(Pet, Owner.owner_id == Pet.owner_id). \
        group_by(Owner, Person).all()

        #google charts table data here
        owner_data = []
        for owner in owners:
            owner_id = owner[0].owner_id
            name = f"{owner.Person.name} {owner.Person.lastname}"
            pet_count = owner[2]
            owner_data.append([owner_id, name, int(pet_count)])

        #Google charts trend data here
        
        persons = db.session.query(Person).all()
        
        trend_data = [{'created': str(person.created), 'count': 1} for person in persons]
        current_date = dt.today()
        min_date = current_date - timedelta(days=4 * 30) 


        #Piechart data

        data = [
            ['Users', 'User count chart'],
            ['Owners', owner_count],
            ['Vets', vet_count],
            ['Editors', editor_count],
            ['Admins', admin_count],
            ['Regular users', other_users]
        ]

        return render_template('login/admin.html',
                                choice = choice,
                                action=action,
                                data = data,
                                owner_data = owner_data,
                                trend_data = trend_data,
                                current_date = current_date,
                                min_date = min_date)

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
            outerjoin(Visit, Visit.vet_id == Vet.vet_id).filter(Vet.active == True). \
            group_by(Vet, Person).all()
        
        return render_template('login/admin.html',
                                choice=choice,
                                action=action,
                                users=users) 
    if choice == 5:
        users = db.session.query(Editor, Person, func.count(Post.post_id)  # Adding the pet counter
        ).join(Person, Editor.person_id == Person.id). \
            outerjoin(Post, Post.editor_id == Editor.editor_id).filter(Editor.active == True). \
            group_by(Editor, Person).all()

        return render_template('login/admin.html',
                                choice=choice,
                                action=action,
                                users=users) 
    if choice == 6:

        vet_person = aliased(Person)
        owner_person = aliased(Person)

        visits = db.session.query(
        Visit, Vet, Owner, Pet, vet_person.name.label('vet_name'), vet_person.lastname.label('vet_lastname'),
        owner_person.name.label('owner_name'), owner_person.lastname.label('owner_lastname'), Pet.name.label('pet_name')
        ).join(Vet, Vet.vet_id == Visit.vet_id) \
        .join(Owner, Owner.owner_id == Visit.owner_id) \
        .join(Pet, Pet.pet_id == Visit.pet_id) \
        .join(vet_person, vet_person.id == Vet.person_id) \
        .join(owner_person, owner_person.id == Owner.person_id).all()

        return render_template('login/admin.html', choice=choice, action=action, visits=visits)
    
    if choice == 7:
        '''pets = db.session.query(Pet, Owner, Person).join(
            Owner, Pet.owner_id == Owner.owner_id
        ).join(
            Person, and_(Owner.person_id == Person.id)
        ).all()'''
        
        pets = db.session.query(Pet, Pet_species, Pet_breed, Owner, Person).\
            join(Pet_species, Pet.pet_species == Pet_species.species_id).\
            join(Pet_breed, Pet.pet_breed == Pet_breed.breed_id).\
            join(Owner, Pet.owner_id == Owner.owner_id).\
            join(Person, and_(Owner.person_id == Person.id)).\
            all()
        return render_template('login/admin.html', choice = choice, pets = pets)

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
    if current_user.type != 2:
        abort(404)
        

    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        mail = request.form.get('mail')
        type = request.form.get('type')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        try:
            person = db.session.query(Person).filter_by(id=person_id).one()

            previous_person_type = person.type
            
            person.name = name
            person.lastname = lastname
            person.mail = mail
            person.type = type
            person.address = address
            person.phone = phone
            choice = 8
            #Am using action in vets for identifiend speciality, action is needed for routing
            action = 0
            if len(phone) == 9:
                db.session.commit()
                if int(type) == 1:  # Regular user

                    choice = 5  #Choice for redirections
                    
                    if previous_person_type == 2:
                        try:
                            admin = db.session.query(Admin).filter_by(person_id=person_id).one()
                            admin.active = False
                        except NoResultFound:
                            pass
                    
                    # Sets previous role's active status to False (Vet and Editor)
                    if previous_person_type == 3:
                        try:
                            vet = db.session.query(Vet).filter_by(person_id=person_id).one()
                            vet.active = False
                        except NoResultFound:
                            pass

                    if previous_person_type == 4:
                        try:
                            editor = db.session.query(Editor).filter_by(person_id=person_id).one()
                            editor.active = False
                        except NoResultFound:
                            pass
                
                if int(type) == 2:  # Admin
                    try:
                        choice = 6  # Or any other choice number for admin
                        admin = db.session.query(Admin).filter_by(person_id=person_id).one()
                        admin.active = True
                    except NoResultFound:
                        admin = Admin(person_id=person_id, active=True)
                        db.session.add(admin)
                    
                    # Sets previous role's active status to False (Vet and Editor)
                    if previous_person_type == 3:
                        try:
                            vet = db.session.query(Vet).filter_by(person_id=person_id).one()
                            vet.active = False
                        except NoResultFound:
                            pass
                    if previous_person_type == 4:
                        try:
                            editor = db.session.query(Editor).filter_by(person_id=person_id).one()
                            editor.active = False
                        except NoResultFound:
                            pass

                elif int(type) == 3:  # Vet
                    try:
                        choice = 4
                        vet = db.session.query(Vet).filter_by(person_id=person_id).one()
                        vet_speciality = request.form.get('vet_speciality')
                        if vet_speciality != None or vet_speciality != 0 or vet_speciality != '0':
                            vet.spec_id = vet_speciality
                        vet.active = True
                        action = vet_speciality
                    except NoResultFound:
                        vet = Vet(person_id=person_id, active=True)
                        db.session.add(vet)

                    # Set previous role's active status to False (Editor)
                    if previous_person_type == 2:
                        try:
                            admin = db.session.query(Admin).filter_by(person_id=person_id).one()
                            admin.active = False
                        except NoResultFound:
                            pass
                    
                    if previous_person_type == 4:
                        try:
                            editor = db.session.query(Editor).filter_by(person_id=person_id).one()
                            editor.active = False
                        except NoResultFound:
                            pass

                elif int(type) == 4:  # Editor
                    try:
                        choice = 5
                        editor = db.session.query(Editor).filter_by(person_id=person_id).one()
                        editor.active = True
                    except NoResultFound:
                        editor = Editor(person_id=person_id, active=True)
                        db.session.add(editor)

                    # Set previous role's active status to False (Vet)
                    if previous_person_type == 2:
                        try:
                            admin = db.session.query(Admin).filter_by(person_id=person_id).one()
                            admin.active = False
                        except NoResultFound:
                            pass

                    if previous_person_type == 3:
                        try:
                            vet = db.session.query(Vet).filter_by(person_id=person_id).one()
                            vet.active = False
                        except NoResultFound:
                            pass


                db.session.commit()

            else:
                flash(f"The number {phone} is not equal to 9", category='error')

        except NoResultFound:
            flash("User not found.", category='error')

        return redirect(url_for('general_logic.admin_logic', choice=choice, action=action))


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
            #breed = request.form.get('breed')
            recent_vaccination = request.form.get('recent_vaccination')
            if name is not None and name != '':
                pet.name = name
                db.session.commit()
                changed = True
                
            '''if species is not None:
                pet.species = species
                db.session.commit()
                changed = True'''
                
            '''if breed is not None and breed != '':
                pet.breed = breed
                db.session.commit()
                changed = True'''

            if recent_vaccination is not None and recent_vaccination != '':
                pet.recent_vaccination = recent_vaccination
                db.session.commit()
                changed = True
            if changed:
                flash('მონაცემები წარმატებით შეიცვალა', category='success')
            if current_user.type == 1:
                return redirect(url_for('general_logic.owner_logic', action=1))
            elif current_user.type == 2:
                return redirect(url_for('general_logic.admin_logic', choice = 1, action=1))
        #return render_template('owner.html', action=action, pet=pet, changed=changed)

    #flash('Pet not found.')
    return redirect(url_for('general_logic.owner_logic', action=action))


@general_logic.route('delete/<int:action>/<int:pet_id>', methods=['GET', 'DELETE'])
@login_required
def remove_pet(action, pet_id):
    pet = db.session.query(Pet).filter_by(pet_id=pet_id).one_or_none()
    history = db.session.query(Pet_history).filter_by(pet_id = pet.pet_id).all( )
    if pet is not None:
        owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
        if owner is not None:
            try:
                if history:
                    for h in history:
                        db.session.delete(h)
                db.session.delete(pet)
                db.session.commit()
                
                remaining_pets = db.session.query(Pet).filter_by(owner_id=owner.owner_id).all()
                if not remaining_pets:
                    db.session.delete(owner)
                    db.session.commit()
                
            except Exception as e:
                flash(e)
        if current_user.type == 1:
            return redirect(url_for('general_logic.owner_logic', action=1))
        if current_user.type == 2:
            return redirect(url_for('general_logic.admin_logic',choice = 1, action=1))
    else:
        abort(404)


@general_logic.route('/get_pet_breeds', methods=['POST'])
def get_pet_breeds():
    # Get the selected species_id from the frontend
    species_id = request.json['species_id']

    # Retrieve the pet breeds for the selected species_id
    pet_breeds = Pet_breed.query.filter_by(species_id=species_id).all()

    # Prepare a list of breed names to send to the frontend
    breed_list = [breed.breed for breed in pet_breeds]

    return jsonify(breed_list)


@general_logic.route('/delete/<int:history_id>', methods=['GET', 'DELETE'])
@login_required
def delete_history(history_id):
    pet_history = db.session.query(Pet_history).filter_by(history_id = history_id).one_or_none()
    if pet_history:
        db.session.delete(pet_history)
        db.session.commit()
        if current_user.type == 1:
            return redirect(url_for('general_logic.owner_logic', action=2))
        if current_user.type == 2:
            return redirect(url_for('general_logic.admin_logic',choice = 1, action=2))
        else:
            abort(404)