from flask import (Blueprint, render_template,
                request, flash, redirect, url_for,
                jsonify, abort)
from flask_login import login_required, current_user
from sqlalchemy import join, select, or_, func, and_, cast, String
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound
from datetime import date as dt, timedelta

from .views import grant_access


from . import db
from .models import *
import logging
import json


general_logic = Blueprint('general_logic', __name__)


#user allowence decorator (does not work as intended)



#User Logics section
edit_mode = False

@general_logic.route('/owner/<int:action>', methods=['GET', 'POST'])
@login_required
@grant_access([1])
def owner_logic(action):
        if action == 0:
            if request.method =="POST":
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                address = request.form.get('address')
                changed = change_user_data(firstname, lastname, address)
                if changed:
                    flash('მონაცემები წარმატებით შეიცვალა.', category='success')
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
            try:
                clinics_data = db.session.query(Clinic).all()
            except:
                clinics_data = None
            if clinics_data:   
                clinics = []
                for clinic in clinics_data:
                    # Check if coordinates is a non-empty string and contains a comma
                    if isinstance(clinic.coordinates, str) and ',' in clinic.coordinates:
                        try:
                            latitude_str, longitude_str = clinic.coordinates.split(",")
                            latitude = float(latitude_str)
                            longitude = float(longitude_str)
                        except ValueError as e:
                            # Log the error and the offending coordinates string
                            logging.warning(f"Invalid coordinates format for clinic {clinic.clinic_name}: {clinic.coordinates}")
                            logging.warning(e)
                            # Skip this clinic and continue with the next
                            continue
                    else:
                        # Log a warning for clinics without valid coordinates
                        logging.warning(f"No valid coordinates provided for clinic {clinic.clinic_name}")
                        # Skip this clinic and continue with the next
                        continue

                    clinic_info = {
                        'clinic_name': clinic.clinic_name,
                        'description': clinic.desc,
                        'clinic_id': clinic.clinic_id,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    clinics.append(clinic_info)
                # Now pass 'clinics' to your template
                logging.warning(clinics)
                return render_template('login/owner.html', clinics=clinics, action=action)

        
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

            return redirect(url_for('general_logic.owner_logic', action=1))
        
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
                

@general_logic.route('/admin/<int:choice>/<int:action>', methods=['GET', 'POST'])
@login_required
@grant_access([2])
def admin_logic(choice, action):
    if choice == 0:
        # Handle search functionality here
        if action == 0:
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
            else:
                search_results = []

        elif action == 1:
            # When action is 1, display all persons
            search_results = db.session.query(Person).all()

        return render_template('login/admin.html', choice=choice, action=action, result = search_results)

    
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
            try:
                clinics_data = db.session.query(Clinic).all()
            except:
                clinics_data = None
            if clinics_data:   
                clinics = []
                for clinic in clinics_data:
                    # Check if coordinates is a non-empty string and contains a comma
                    if isinstance(clinic.coordinates, str) and ',' in clinic.coordinates:
                        try:
                            latitude_str, longitude_str = clinic.coordinates.split(",")
                            latitude = float(latitude_str)
                            longitude = float(longitude_str)
                        except ValueError as e:
                            # Log the error and the offending coordinates string
                            logging.warning(f"Invalid coordinates format for clinic {clinic.clinic_name}: {clinic.coordinates}")
                            logging.warning(e)
                            # Skip this clinic and continue with the next
                            continue
                    else:
                        # Log a warning for clinics without valid coordinates
                        logging.warning(f"No valid coordinates provided for clinic {clinic.clinic_name}")
                        # Skip this clinic and continue with the next
                        continue

                    clinic_info = {
                        'clinic_name': clinic.clinic_name,
                        'description': clinic.desc,
                        'clinic_id': clinic.clinic_id,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    clinics.append(clinic_info)
                # pass ing'clinics' to your template
                return render_template('login/admin.html', clinics=clinics, action=action, choice=choice)

        
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
                else:
                    return render_template('login/admin.html', choice = choice, action = 6, pets = None)
            elif request.method == "POST":
                pet_id = request.form.get('pet_name')
                treatment = request.form.get('treatment')
                comment = request.form.get('comment')
                date = request.form.get('date')
                new_history = Pet_history(pet_id = pet_id, treatment = treatment,
                                        date = date, comment = comment)
                db.session.add(new_history)
                db.session.commit()
                return redirect(url_for('general_logic.admin_logic', choice=choice, action=2))
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

        #Admin notes
        notes = db.session.query(Note).filter_by(person_id = current_user.id).all()
        return render_template('login/admin.html',
                            choice = choice,
                            action=action,
                            data = data,
                            owner_data = owner_data,
                            trend_data = trend_data,
                            current_date = current_date,
                            min_date = min_date,
                            notes = notes)
        
            

    if choice == -1:
        users = db.session.query(Owner, Person, func.count(Pet.pet_id)  # Adding the pet counter
        ).join(Person, Owner.person_id == Person.id). \
            outerjoin(Pet, Owner.owner_id == Pet.owner_id). \
            group_by(Owner, Person).all()
        
        return render_template('login/admin.html',
                                choice=choice,
                                action=action,
                                users=users)
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
                flash('მონაცემები წარმატებით შეიცვალა.', category='success')
            return render_template('login/admin.html',choice = choice, action = action)

    return render_template('login/admin.html', choice = choice)


@general_logic.route('/vet/<int:choice>/<int:action>', methods=['GET', 'POST'])
@login_required
@grant_access([3])
def vet_logic(choice, action):
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

        return render_template('login/vet.html', choice=choice, action = search_results)

    if choice == 1:
        if action == 1:
            # მფლობელის მონაცემების მიღება და მფლობელის ID-ის მიხედვით
            owner = db.session.query(Owner).filter_by(person_id=current_user.id).one_or_none()
            if owner is None:
                return render_template('login/vet.html',choice = choice, action=action, pets=None)
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
                    return render_template('login/vet.html',
                                           choice = choice ,action=action, pets=None)
                else:
                    return render_template('login/vet.html',
                                           choice = choice, action=action, pets=pets)
                
        elif action == 2:
            owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
            if owner:
                pet_history = db.session.query(Pet_history, Pet).\
                    join(Pet, Pet_history.pet_id == Pet.pet_id).\
                    filter(Pet.owner_id == owner.owner_id).all()
                if request.method == "GET":
                    return render_template('login/vet.html',
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

                    return render_template('login/vet.html',
                                    choice = choice, action = action,
                                    pet_history = pet_history)
            else:
                return render_template('login/vet.html',
                                    choice = choice, action = action,
                                    pet_history = None)

        
        elif action == 3:
            try:
                clinics_data = db.session.query(Clinic).all()
            except:
                clinics_data = None
            if clinics_data:   
                clinics = []
                for clinic in clinics_data:
                    # Check if coordinates is a non-empty string and contains a comma
                    if isinstance(clinic.coordinates, str) and ',' in clinic.coordinates:
                        try:
                            latitude_str, longitude_str = clinic.coordinates.split(",")
                            latitude = float(latitude_str)
                            longitude = float(longitude_str)
                        except ValueError as e:
                            # Log the error and the offending coordinates string
                            logging.warning(f"Invalid coordinates format for clinic {clinic.clinic_name}: {clinic.coordinates}")
                            logging.warning(e)
                            # Skip this clinic and continue with the next
                            continue
                    else:
                        # Log a warning for clinics without valid coordinates
                        logging.warning(f"No valid coordinates provided for clinic {clinic.clinic_name}")
                        # Skip this clinic and continue with the next
                        continue

                    clinic_info = {
                        'clinic_name': clinic.clinic_name,
                        'description': clinic.desc,
                        'clinic_id': clinic.clinic_id,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    clinics.append(clinic_info)
                # Now pass 'clinics' to your template
                logging.warning(clinics)
                return render_template('login/vet.html', clinics=clinics, action=action, choice=choice)

        
        elif action == 4:
            vets = db.session.query(Vet, Person).join(Person, Vet.person_id == Person.id).filter(Vet.active == True).all()
            return render_template('login/vet.html',
                                    choice = choice, action=action,
                                    vets = vets)
        
        elif action == 5:
            if request.method == "GET":
                pet_species_list = db.session.query(Pet_species).all()
                return render_template('login/vet.html', choice = choice, action = action, pet_species_list = pet_species_list)
            
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

            return redirect(url_for('general_logic.vet_logic', choice=choice, action=1))

        elif action == 6: #needs pets from current user
            if request.method == "GET":    
                owner = db.session.query(Owner).filter_by(person_id = current_user.id).one_or_none()
                if owner:
                    pets = db.session.query(Pet).filter_by(owner_id = owner.owner_id).all()
                    return render_template('login/vet.html',
                                    choice = choice, action = 6, pets = pets)
                else:
                    return render_template('login/vet.html', choice = choice, action = action, pets = None)
            elif request.method == "POST":
                pet_id = request.form.get('pet_name')
                treatment = request.form.get('treatment')
                comment = request.form.get('comment')
                date = request.form.get('date')
                new_history = Pet_history(pet_id = pet_id, treatment = treatment,
                                        date = date, comment = comment)
                db.session.add(new_history)
                db.session.commit()
                return redirect(url_for('general_logic.vet_logic', choice=choice, action=2))
        else:
            return render_template('login/vet.html', choice=1, action=None)

    if choice == 2: #dashboard
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

        #Admin notes
        notes = db.session.query(Note).filter_by(person_id = current_user.id).all()
        return render_template('login/admin.html',
                            choice = choice,
                            action=action,
                            data = data,
                            owner_data = owner_data,
                            trend_data = trend_data,
                            current_date = current_date,
                            min_date = min_date,
                            notes = notes)
        
    if choice == 4: #My visits
        if action == 0:
            if request.method == "POST":
                clinic = request.form.get('clinic')
                vet_id = request.form.get('vet')
                owner_id = request.form.get('ownerId')
                pet_id = request.form.get('petId')
                diagnosis = request.form.get('diagnosis')
                treatment = request.form.get('treatment')
                date = request.form.get('date')
                if not date:
                    date = dt.today()
                comment = request.form.get('comment')

                visit = Visit(clinic_id = clinic, vet_id = vet_id,
                              owner_id = owner_id, pet_id = pet_id,
                              diagnosis = diagnosis, treatment = treatment,
                              comment = comment, date = date)

                db.session.add(visit)
                db.session.commit()

            elif request.method == "GET":
                try:
                    # Querying bridges and getting clinics to work with
                    # Js catches data and responsively gives out options
                    my_clinics = db.session.query(
                        P_C_bridge.clinic_id).filter_by(
                        person_id=current_user.id).all()

                    clinic_ids = [bridge.clinic_id for bridge in my_clinics]

                    staff_members_by_clinic = {}
                    for clinic_id in clinic_ids:
                        # Query for staff members at this clinic
                        staff_members = db.session.query(Person).join(
                            P_C_bridge, P_C_bridge.person_id == Person.id).filter(
                            P_C_bridge.clinic_id == clinic_id,
                            P_C_bridge.person_id != current_user.id).all()

                        # Add the staff members to the dictionary, keyed by clinic_id
                        staff_members_by_clinic[clinic_id] = staff_members

                    clinics = db.session.query(Clinic).filter(Clinic.clinic_id.in_(clinic_ids)).all()

                                        
                    return render_template('login/vet.html',action=action, choice=choice,
                                clinics=clinics,
                                staff_members_by_clinic=staff_members_by_clinic)

                except Exception as e:
                    logging.warning(e)
                return render_template('login/vet.html',
                            action=action, choice=choice, clinics = None, staff_members = None)
            
                
        elif action == 1:
            vet_person = aliased(Person)
            owner_person = aliased(Person)
            vet = db.session.query(Vet).filter_by(person_id = current_user.id).one_or_none()
            if vet:
                visits = db.session.query(
                Visit, Vet, Owner, Pet, vet_person.name.label('vet_name'), vet_person.lastname.label('vet_lastname'),
                owner_person.name.label('owner_name'), owner_person.lastname.label('owner_lastname'), Pet.name.label('pet_name')
                ).join(Vet, Vet.vet_id == Visit.vet_id) \
                .join(Owner, Owner.owner_id == Visit.owner_id) \
                .join(Pet, Pet.pet_id == Visit.pet_id) \
                .join(vet_person, vet_person.id == Vet.person_id) \
                .join(owner_person, owner_person.id == Owner.person_id).filter(Visit.vet_id == vet.vet_id).all()

                return render_template('login/vet.html', choice=choice, action=action, visits=visits)
            else:
                return render_template('login/vet.html', choice=choice, action=action, visits=None)



    if choice == 5: #Add my clinic
        if action == 0:
            if request.method == "POST":
                clinic_name = request.form.get('clinic-name')
                desc = request.form.get('comment')
                coordinates = request.form.get('coordinates')
                try:
                    edit_mode = request.form.get('edit_mode')
                    clinic_id = request.form.get('clinic_id')
                    clinic = db.session.query(Clinic).filter_by(clinic_id = clinic_id).one_or_none()
                    if edit_mode:
                        if clinic:
                            clinic.clinic_name = clinic_name
                            clinic.desc = desc
                            clinic.coordinates = coordinates
                            db.session.commit()
                            return redirect(url_for('general_logic.vet_logic', choice=choice, action=1))
                except:
                    logging.warning('Editmode is False or nonexistant')
                try:
                    clinic = Clinic(clinic_name = clinic_name, desc = desc, coordinates = coordinates)
                    db.session.add(clinic)
                    db.session.commit()
                    clinic_id = clinic.clinic_id
                    #adding mixture
                    pc_bridge = P_C_bridge(person_id = current_user.id, 
                                        clinic_id = clinic_id, is_clinic_owner = True)
                    db.session.add(pc_bridge)
                    db.session.commit()
                    flash("კლინიკა წარმატებით დაემატა", category='success')
                    return redirect(url_for('general_logic.vet_logic', choice=choice, action=1))
                except Exception as e:
                    flash(f"გაუთვალისწინებელი ლოგიკის პრობლემა: {e}")

            elif request.method == "GET":
                try:
                    clinic_id = request.args.get('clinic_id')
                    if clinic_id:
                        clinic = db.session.query(Clinic).filter_by(clinic_id = clinic_id).one_or_none()
                        if clinic:
                            return render_template('login/vet.html',
                                    action=action, choice=choice, edit_mode=True, clinic=clinic)
                        
                except Exception as e:
                    logging.warning(e)
                return render_template('login/vet.html',
                                    action=action, choice = choice, edit_mode = False, clinic=None)
        elif action == 1:
            if request.method == "GET":
                try:
                    # Query P_C_bridge to get clinic and personel IDs
                    my_bridge = db.session.query(P_C_bridge).filter_by(person_id=current_user.id).all()
                    clinics = []
                    personels = []
                    for bridge in my_bridge:
                        clinic = db.session.query(Clinic).filter_by(clinic_id=bridge.clinic_id).one_or_none()
                        if clinic:
                            clinics.append(clinic)
                            
                        # Joining P_C_bridge with persons to get personel data
                        personel = db.session.query(Person).join(P_C_bridge).filter(
                            P_C_bridge.person_id == Person.id,
                            P_C_bridge.bridge_id == bridge.bridge_id,
                            P_C_bridge.is_clinic_owner == False
                            ).one_or_none()

                        if personel:
                            personels.append(personel)
                    return render_template('login/vet.html',
                                           choice = choice, action = action, 
                                           clinics = clinics, personels = personels)

                except Exception as e:
                    logging.warning(e)
              
        else:
            abort(404)


    if choice == 8: #My Data
        if request.method =="POST":
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            address = request.form.get('address')
            changed = change_user_data(firstname, lastname, address)
            if changed:
                flash('მონაცემები წარმატებით შეიცვალა.', category='success')
            return render_template('login/vet.html',choice = choice, action = action)

    return render_template('login/vet.html', choice = choice)

#Addition functions section


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


@general_logic.route('/add_new_note', methods=['POST'])
@grant_access([2])
def add_note(): 
    #category = request.form.get('icon_option')
    note = request.form.get('note')
    person_id = current_user.id
    created = dt.today()
    new_note = Note(person_id = person_id, created = created, content = note)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('general_logic.admin_logic', choice = 2, action = 0))




#Getting data functions section


@general_logic.route('/get_pet_breeds', methods=['POST'])
def get_pet_breeds():
    # Get the selected species_id from the frontend
    species_id = request.json['species_id']

    # Retrieve the pet breeds for the selected species_id
    pet_breeds = Pet_breed.query.filter_by(species_id=species_id).all()

    # Prepare a list of breed names to send to the frontend
    breed_list = [breed.breed for breed in pet_breeds]

    return jsonify(breed_list)


#Editing functions section


@general_logic.route('edit/<int:action>/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(action, pet_id):
    pet = db.session.query(Pet).filter_by(pet_id = pet_id).one_or_none()
    changed = False
    if pet:
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
                return redirect(url_for('general_logic.admin_logic', choice=1, action=1))
            elif current_user.type == 3:
                return redirect(url_for('general_logic.vet_logic', choice=1, action=1))
        #return render_template('owner.html', action=action, pet=pet, changed=changed)

    #flash('Pet not found.')
    return redirect(url_for('general_logic.owner_logic', action=action))


@general_logic.route('/admin/edit_user/<int:person_id>', methods=['GET', 'POST'])
@login_required
@grant_access([2])
def edit_user(person_id):
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        mail = request.form.get('mail')
        type = request.form.get('type')
        address = request.form.get('address')
        phone = request.form.get('phone')
        choice = 0

        try:
            person = db.session.query(Person).filter_by(id=person_id).one()

            previous_person_type = person.type
            
            person.name = name
            person.lastname = lastname
            person.mail = mail
            person.type = type
            person.address = address
            person.phone = phone
            #Am using action in vets for identifiend speciality, result is needed for routing
            db.session.commit()
            if int(type) == 1:  # Regular user
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

        except NoResultFound:
            flash("მომხმარებელი ვერ მოიძებნა.", category='error')
        action = request.form.get('action')
        action = int(action)
        return redirect(url_for('general_logic.admin_logic', choice=choice, action=action))


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


@general_logic.route('edit/<int:action>/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = db.session.query(Note).filter_by(note_id = note_id).one_or_none()
    new_note = request.form.get('comment')
    note.note = new_note
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash("შეცდომა.", category='error')
    return redirect(url_for('general_logic.admin_logic', choice = 2, action=0))


#Removing functions section


@general_logic.route('/remove_pet/<int:action>/<int:pet_id>', methods=['GET', 'DELETE'])
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
        elif current_user.type == 2:
            return redirect(url_for('general_logic.admin_logic',choice = 1, action=1))
        elif current_user.type == 3:
            return redirect(url_for('general_logic.vet_logic', choice=1, action=1))
    else:
        abort(404)


@general_logic.route('/remove_history/<int:history_id>', methods=['GET', 'DELETE'])
@login_required
def remove_history(history_id):
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


@general_logic.route('/remove_note/<int:note_id>', methods=['GET', 'DELETE'])
@login_required
@grant_access([2])
def remove_note(note_id):
    admin_note = db.session.query(Note).filter_by(note_id = note_id).one_or_none()
    if admin_note:
        db.session.delete(admin_note)
        db.session.commit()
        return redirect(url_for('general_logic.admin_logic',choice = 2, action=0))

    else:
        return redirect(url_for('general_logic.admin_logic',choice = 2, action=0))
    


