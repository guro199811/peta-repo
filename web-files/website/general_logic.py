from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    abort,
)
from flask_login import login_required, current_user
from datetime import date as dt, timedelta
from flask_babel import _
from .views import grant_access
from . import db
from .models import (
    Person,
    Owner,
    Clinic,
    Vet,
    PersonToClinic,
    PetSpecies,
    PetBreed,
    Pet,
    PetHistory,
    Admin,
    Editor,
    Visit,
    Note,
    Requests,
)
import json
from .logs import logger_config

logger = logger_config.logger

general_logic = Blueprint("general_logic", __name__)
# User Logics section


@general_logic.route("/owner/<int:action>", methods=["GET", "POST"])
@login_required
@grant_access([1])
def owner_logic(action):
    """
    This function handles the owner(user) actions.

    Parameters:
    action (int): The action to be performed by the owner.

    Returns:
    -> render_template: The rendered HTML template for the owner's action.
       or
    -> redirect: Redirects the user to the appropriate page.
    """
    match action:
        case 0:
            if request.method == "POST":
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                address = request.form.get("address")
                changed = change_user_data(firstname, lastname, address)
                if changed:
                    flash(
                        _("მონაცემები წარმატებით შეიცვალა."),
                        category="success",
                    )
                return render_template("login/owner.html", action=action)

            return render_template("login/owner.html", action=action)
        case 1:
            # Owner data is being retrieved with current user_id
            owner = Owner.get_owner(current_user.id)
            if owner is None:
                return render_template(
                    "login/owner.html", action=action, pets=None
                )
            else:
                # Retrieving Pet data using Owner Data
                pets = Pet.get_pets_extended(owner.owner_id)
                if len(pets) == 0:
                    return render_template(
                        "login/owner.html", action=action, pets=None
                    )
                else:
                    return render_template(
                        "login/owner.html", action=action, pets=pets
                    )

        case 2:
            owner = Owner.get_owner(current_user.id)
            if owner:
                pet_history = PetHistory.get_history_by_owner(owner.owner_id)
                try:
                    visits = Visit.get_visits(current_user.id)
                except Exception as e:
                    visits = None
                    logger.exception(f'{e.__class__.__name__} -> {e}')

                if request.method == "GET":
                    return render_template(
                        "login/owner.html",
                        action=action,
                        pet_history=pet_history,
                        visits=visits,
                    )
                elif request.method == "POST":
                    history_id = request.form.get("history_id")
                    treatment = request.form.get("treatment")
                    comment = request.form.get("comment")
                    date = request.form.get("date")

                    history = PetHistory.get_history_by_hist_id(history_id)
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

                    return render_template(
                        "login/owner.html",
                        action=action,
                        pet_history=pet_history,
                    )
            else:
                return render_template(
                    "login/owner.html", action=action, pet_history=None
                )
        case 3:
            try:
                clinics_data = Clinic.get_all_visible_clinics()
            except Exception as e:
                logger.exception(f'{e.__class__.__name__} -> {e}')
                clinics_data = None
            if clinics_data:
                clinics = []
                for clinic in clinics_data:
                    # Check if coordinates is a
                    # non-empty string and contains a comma
                    if (
                        isinstance(clinic.coordinates, str)
                        and "," in clinic.coordinates
                    ):
                        try:
                            latitude_str, longitude_str = (
                                clinic.coordinates.split(",")
                            )
                            latitude = float(latitude_str)
                            longitude = float(longitude_str)
                        except ValueError as e:
                            # Skip this clinic and continue with the next
                            logger.exception(f'{e.__class__.__name__} -> {e}')
                            continue
                    else:
                        # Skip this clinic
                        continue

                    clinic_info = {
                        "clinic_name": clinic.clinic_name,
                        "description": clinic.desc,
                        "clinic_id": clinic.clinic_id,
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                    clinics.append(clinic_info)
                # logger.debug(clinics)
                return render_template(
                    "login/owner.html", clinics=clinics, action=action
                )
            return render_template(
                "login/owner.html", clinics=None, action=action
            )

        case 4:
            vets = Vet.get_all_vets()
            return render_template(
                "login/owner.html", action=action, vets=vets
            )

        case 5:
            if request.method == "GET":
                pet_species_list = PetSpecies.get_all_species()
                return render_template(
                    "login/owner.html",
                    action=action,
                    pet_species_list=pet_species_list,
                )

            if request.method == "POST":
                pet_name = request.form.get("pet_name")
                pet_species = request.form.get("pet_species")
                pet_breed = request.form.get("pet_breed")
                recent_vaccination = request.form.get("recent_vaccination")
                gender = request.form.get("gender")
                birth_date = request.form.get("bdate")

                confirmation = register_pet(
                    pet_name,
                    pet_species,
                    pet_breed,
                    recent_vaccination,
                    gender,
                    birth_date,
                )
                if confirmation:
                    flash(
                        _("ცხოველი დარეგისტრირდა წარმატებით"),
                        category="success",
                    )
                else:
                    flash(
                        _("თქვენი ცხოველი ვერ დარეგისტრირდა"),
                        category="error",
                    )

            return redirect(url_for("general_logic.owner_logic", action=1))

        case 6:  # needs pets from current user
            if request.method == "GET":
                owner = Owner.get_owner(current_user.id)
                if owner:
                    pets = Pet.get_pets(owner.owner_id)
                    return render_template(
                        "login/owner.html", action=6, pets=pets
                    )
                else:
                    return render_template(
                        "login/owner.html", action=6, pets=None
                    )
            elif request.method == "POST":
                pet_id = request.form.get("pet_name")
                treatment = request.form.get("treatment")
                comment = request.form.get("comment")
                date = request.form.get("date")
                new_history = PetHistory(
                    pet_id=pet_id,
                    treatment=treatment,
                    date=date,
                    comment=comment,
                )
                db.session.add(new_history)
                db.session.commit()
                return redirect(url_for("general_logic.owner_logic", action=2))

        case _:
            abort(404)


@general_logic.route(
    "/admin/<int:choice>/<int:action>", methods=["GET", "POST"]
)
@login_required
@grant_access([2])
def admin_logic(choice, action):
    """
    This function handles the admin(user) dashboard.
    It processes different actions based on the choice and action parameters.

    Parameters:
    choice (int): The choice selected by the admin user.
    action (int): The action selected by the admin user.

    Returns:
    -> render_template: A rendered HTML template
       based on the choice and action parameters.
    or
    -> redirect: A redirect to the appropriate page.
    """
    match choice:
        case 0:
            # Handle search functionality here
            if action == 0:
                search_query = request.args.get("q")
                if search_query:
                    # Perform a case-insensitive search on the 'persons' table
                    search_query = f"%{search_query.lower()}%"
                    search_results = Person.search_users(search_query)
                else:
                    search_results = []

            elif action == 1:
                # When action is 1, display all persons
                search_results = Person.get_all_users()

            return render_template(
                "login/admin.html",
                choice=choice,
                action=action,
                result=search_results,
            )

        case 1:
            match action:
                case 1:
                    owner = Owner.get_owner(current_user.id)
                    if owner is None:
                        return render_template(
                            "login/admin.html",
                            choice=choice,
                            action=action,
                            pets=None,
                        )
                    else:
                        pets = pets = Pet.get_pets_extended(owner.owner_id)

                        if len(pets) == 0:
                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=action,
                                pets=None,
                            )
                        else:
                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=action,
                                pets=pets,
                            )

                case 2:
                    owner = Owner.get_owner(current_user.id)
                    if owner:
                        pet_history = PetHistory.get_history_by_owner(
                            owner.owner_id
                        )
                        try:
                            visits = Visit.get_visits(current_user.id)
                        except Exception as e:
                            logger.exception(f'{e.__class__.__name__} -> {e}')
                            visits = None

                        if request.method == "GET":
                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=action,
                                pet_history=pet_history,
                                visits=visits,
                            )
                        elif request.method == "POST":
                            history_id = request.form.get("history_id")
                            treatment = request.form.get("treatment")
                            comment = request.form.get("comment")
                            date = request.form.get("date")

                            history = PetHistory.get_history_by_hist_id(
                                history_id
                            )
                            if history:
                                if treatment:
                                    history.treatment = treatment
                                if comment:
                                    history.comment = comment
                                if date:
                                    history.date = date
                            db.session.commit()

                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=action,
                                pet_history=pet_history,
                            )
                    else:
                        return render_template(
                            "login/admin.html",
                            choice=choice,
                            action=action,
                            pet_history=None,
                        )

                case 3:
                    try:
                        clinics_data = Clinic.get_all_visible_clinics()
                    except Exception as e:
                        logger.exception(f'{e.__class__.__name__} -> {e}')
                        clinics_data = None
                    if clinics_data:
                        clinics = []
                        for clinic in clinics_data:
                            # Check if coordinates is a non-empty string
                            # and contains a comma
                            if (
                                isinstance(clinic.coordinates, str)
                                and "," in clinic.coordinates
                            ):
                                try:
                                    latitude_str, longitude_str = (
                                        clinic.coordinates.split(",")
                                    )
                                    latitude = float(latitude_str)
                                    longitude = float(longitude_str)
                                except ValueError as e:
                                    logger.exception(
                                        f'{e.__class__.__name__} -> {e}')
                                    continue
                            else:
                                logger.warning(
                                    "No valid coordinates provided for clinic "
                                    + f"{clinic.clinic_name}"
                                )
                                # Skip this clinic and continue with the next
                                continue

                            clinic_info = {
                                "clinic_name": clinic.clinic_name,
                                "description": clinic.desc,
                                "clinic_id": clinic.clinic_id,
                                "latitude": latitude,
                                "longitude": longitude,
                            }
                            clinics.append(clinic_info)
                        # pass ing'clinics' to your template
                        return render_template(
                            "login/admin.html",
                            clinics=clinics,
                            action=action,
                            choice=choice,
                        )
                    return render_template(
                        "login/admin.html",
                        clinics=None,
                        action=action,
                        choice=choice,
                    )

                case 4:
                    vets = Vet.get_all_vets()
                    return render_template(
                        "login/admin.html",
                        choice=choice,
                        action=action,
                        vets=vets,
                    )

                case 5:
                    if request.method == "GET":
                        pet_species_list = PetSpecies.get_all_species()
                        return render_template(
                            "login/admin.html",
                            choice=choice,
                            action=action,
                            pet_species_list=pet_species_list,
                        )

                    if request.method == "POST":
                        pet_name = request.form.get("pet_name")
                        pet_species = request.form.get("pet_species")
                        pet_breed = request.form.get("pet_breed")
                        recent_vaccination = request.form.get(
                            "recent_vaccination"
                        )
                        gender = request.form.get("gender")
                        birth_date = request.form.get("bdate")

                        confirmation = register_pet(
                            pet_name,
                            pet_species,
                            pet_breed,
                            recent_vaccination,
                            gender,
                            birth_date,
                        )
                        if confirmation:
                            flash(
                                _("ცხოველი დარეგისტრირდა წარმატებით"),
                                category="success",
                            )
                        else:
                            flash(
                                _("თქვენი ცხოველი ვერ დარეგისტრირდა"),
                                category="error",
                            )

                    return render_template(
                        "login/admin.html", choice=choice, action=action
                    )

                case 6:  # needs pets from current user
                    if request.method == "GET":
                        owner = Owner.get_owner(current_user.id)
                        if owner:
                            pets = Pet.get_pets(owner.owner_id)
                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=6,
                                pets=pets,
                            )
                        else:
                            return render_template(
                                "login/admin.html",
                                choice=choice,
                                action=6,
                                pets=None,
                            )
                    elif request.method == "POST":
                        pet_id = request.form.get("pet_name")
                        treatment = request.form.get("treatment")
                        comment = request.form.get("comment")
                        date = request.form.get("date")
                        new_history = PetHistory(
                            pet_id=pet_id,
                            treatment=treatment,
                            date=date,
                            comment=comment,
                        )
                        db.session.add(new_history)
                        db.session.commit()
                        return redirect(
                            url_for(
                                "general_logic.admin_logic",
                                choice=choice,
                                action=2,
                            )
                        )

                case _:
                    return render_template(
                        "login/admin.html", choice=1, action=None
                    )

        case 2:
            owner_count = db.session.query(Owner).count()
            vet_count = db.session.query(Vet).filter_by(active=True).count()
            editor_count = (
                db.session.query(Editor).filter_by(active=True).count()
            )
            admin_count = db.session.query(Admin).count()
            other_users = Person.count_unique_users()

            owners = Owner.get_all_owners()

            # google charts table data here
            owner_data = []
            for owner in owners:
                owner_id = owner[0].owner_id
                name = f"{owner.Person.name} {owner.Person.lastname}"
                pet_count = owner[2]
                owner_data.append([owner_id, name, int(pet_count)])

            # Google charts trend data here

            persons = Person.get_all_users()

            trend_data = [
                {"created": str(person.created), "count": 1}
                for person in persons
            ]
            current_date = dt.today()
            min_date = current_date - timedelta(days=4 * 30)

            # Piechart data

            data = [
                ["Users", "User count chart"],
                ["Owners", owner_count],
                ["Vets", vet_count],
                ["Editors", editor_count],
                ["Admins", admin_count],
                ["Regular users", other_users],
            ]

            # Admin notes
            notes = Note.get_admin_notes(current_user.id)
            return render_template(
                "login/admin.html",
                choice=choice,
                action=action,
                data=data,
                owner_data=owner_data,
                trend_data=trend_data,
                current_date=current_date,
                min_date=min_date,
                notes=notes,
            )

        case -1:
            users = Owner.get_all_owners()

            return render_template(
                "login/admin.html", choice=choice, action=action, users=users
            )

        case 3:
            users = Owner.get_all_owners()

            return render_template(
                "login/admin.html", choice=choice, action=action, users=users
            )

        case 4:
            users = Vet.get_grouped_vets()

            return render_template(
                "login/admin.html", choice=choice, action=action, users=users
            )

        case 5:
            users = Editor.get_grouped_editors()

            return render_template(
                "login/admin.html", choice=choice, action=action, users=users
            )

        case 6:
            visits = Visit.get_visits_unfilterd()

            return render_template(
                "login/admin.html",
                choice=choice,
                action=action,
                visits=visits,
            )

        case 7:
            pets = Pet.get_all_pets_extended()

            return render_template(
                "login/admin.html", choice=choice, pets=pets
            )

        case 8:
            if request.method == "POST":
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                address = request.form.get("address")
                changed = change_user_data(firstname, lastname, address)
                if changed:
                    flash(
                        _("მონაცემები წარმატებით შეიცვალა."),
                        category="success",
                    )
                return render_template(
                    "login/admin.html", choice=choice, action=action
                )

        case 9:
            clinics = PersonToClinic.get_all_clinic_owners()

            return render_template(
                "login/admin.html",
                choice=choice,
                action=action,
                clinics=clinics,
            )

    return render_template("login/admin.html", choice=choice)


@general_logic.route(
    "/vet/<int:choice>/<int:action>", methods=["GET", "POST"]
)
@login_required
@grant_access([3])
def vet_logic(choice, action):
    """
    Handle the general logic for the vet dashboard.

    Parameters:
    choice (int): The choice selected by the user.
    action (int): The action selected by the user.

    Returns:
    render_template: The rendered template for the vet dashboard.
    """
    match choice:
        case 0:
            # Handle search functionality here
            search_query = request.args.get("q")
            if search_query:
                # Perform a case-insensitive search on the 'persons' table
                search_query = f"%{search_query.lower()}%"
                search_results = Person.search_users(search_query)

            return render_template(
                "login/vet.html", choice=choice, action=search_results
            )

        case 1:
            if action == 1:
                owner = Owner.get_owner(current_user.id)
                if owner is None:
                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        pets=None,
                    )
                else:
                    pets = pets = Pet.get_pets_extended(owner.owner_id)
                    if len(pets) == 0:
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            pets=None,
                        )
                    else:
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            pets=pets,
                        )

            elif action == 2:
                owner = Owner.get_owner(current_user.id)
                if owner:
                    pet_history = PetHistory.get_history_by_owner(
                        owner.owner_id
                    )
                    try:
                        visits = Visit.get_visits(current_user.id)
                    except Exception as e:
                        visits = None
                        logger.exception(f'{e.__class__.__name__} -> {e}')

                    if request.method == "GET":
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            pet_history=pet_history,
                            visits=visits,
                        )
                    elif request.method == "POST":
                        history_id = request.form.get("history_id")
                        treatment = request.form.get("treatment")
                        comment = request.form.get("comment")
                        date = request.form.get("date")

                        history = PetHistory.get_history_by_hist_id(
                            history_id
                        )
                        if history:
                            if treatment:
                                history.treatment = treatment
                            if comment:
                                history.comment = comment
                            if date:
                                history.date = date
                        db.session.commit()

                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            pet_history=pet_history,
                        )
                else:
                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        pet_history=None,
                    )

            elif action == 3:
                try:
                    clinics_data = Clinic.get_all_visible_clinics()
                except Exception as e:
                    logger.exception(f'{e.__class__.__name__} -> {e}')
                    clinics_data = None
                # TODO Might want to transform this part of code into
                # more reusable, either a function or staticmethod
                if clinics_data:
                    clinics = []
                    for clinic in clinics_data:
                        # Check if coordinates is a non-empty string
                        # and contains a comma
                        if (
                            isinstance(clinic.coordinates, str)
                            and "," in clinic.coordinates
                        ):
                            try:
                                latitude_str, longitude_str = (
                                    clinic.coordinates.split(",")
                                )
                                latitude = float(latitude_str)
                                longitude = float(longitude_str)
                            except ValueError as e:
                                logger.exception(
                                    f'{e.__class__.__name__} -> {e}')
                                # Skip this clinic and continue with the next
                                continue
                        else:
                            continue

                        clinic_info = {
                            "clinic_name": clinic.clinic_name,
                            "description": clinic.desc,
                            "clinic_id": clinic.clinic_id,
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                        clinics.append(clinic_info)
                    return render_template(
                        "login/vet.html",
                        clinics=clinics,
                        action=action,
                        choice=choice,
                    )
                return render_template(
                    "login/vet.html",
                    clinics=None,
                    action=action,
                    choice=choice,
                )

            elif action == 4:
                vets = Vet.get_all_vets()
                return render_template(
                    "login/vet.html", choice=choice, action=action, vets=vets
                )

            elif action == 5:
                if request.method == "GET":
                    pet_species_list = PetSpecies.get_all_species()
                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        pet_species_list=pet_species_list,
                    )

                if request.method == "POST":
                    pet_name = request.form.get("pet_name")
                    pet_species = request.form.get("pet_species")
                    pet_breed = request.form.get("pet_breed")
                    recent_vaccination = request.form.get(
                        "recent_vaccination"
                    )
                    gender = request.form.get("gender")
                    birth_date = request.form.get("bdate")

                    confirmation = register_pet(
                        pet_name,
                        pet_species,
                        pet_breed,
                        recent_vaccination,
                        gender,
                        birth_date,
                    )
                    if confirmation:
                        flash(
                            _("ცხოველი დარეგისტრირდა წარმატებით"),
                            category="success",
                        )
                    else:
                        flash(
                            _("თქვენი ცხოველი ვერ დარეგისტრირდა"),
                            category="error",
                        )

                return redirect(
                    url_for(
                        "general_logic.vet_logic", choice=choice, action=1
                    )
                )

            elif action == 6:  # needs pets from current user
                if request.method == "GET":
                    owner = Owner.get_owner(current_user.id)
                    if owner:
                        pets = Pet.get_pets(owner.owner_id)
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=6,
                            pets=pets,
                        )
                    else:
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            pets=None,
                        )
                elif request.method == "POST":
                    pet_id = request.form.get("pet_name")
                    treatment = request.form.get("treatment")
                    comment = request.form.get("comment")
                    date = request.form.get("date")
                    new_history = PetHistory(
                        pet_id=pet_id,
                        treatment=treatment,
                        date=date,
                        comment=comment,
                    )
                    db.session.add(new_history)
                    db.session.commit()
                    return redirect(
                        url_for(
                            "general_logic.vet_logic", choice=choice, action=2
                        )
                    )
            else:
                return render_template(
                    "login/vet.html", choice=1, action=None
                )

        case 3:  # Requests
            sent_requests = Requests.get_sent_requests(current_user.id)
            recieved_requests = Requests.get_received_requests(current_user.id)

            sent_connections = get_clinic_by_request(sent_requests)
            received_connections = get_clinic_by_request(recieved_requests)

            return render_template(
                "login/vet.html",
                sentRequests=sent_connections,
                recievedRequest=received_connections,
                action=action,
                choice=choice,
            )

        case 4:  # My visits
            if action == 0:
                if request.method == "POST":
                    clinic = request.form.get("clinic")
                    person = request.form.get("vet")
                    vet = Vet.get_vet(current_user.id)
                    if vet is None:
                        flash(
                            _(
                                "ვეტერინარი არ არის დარეგისტრირებული\
                                ვეტერინარულ ბაზაში\n\
                                გთხოვთ მიმართოს ადმინისტრაციას"
                            )
                        )

                    owner_id = request.form.get("ownerId")
                    pet_id = request.form.get("petId")
                    if owner_id is None:
                        flash(_("გთხოვთ მიუთითოთ შინაური ცხოველის პატრონი."))
                    if pet_id is None:
                        flash(_("გთხოვთ მიუთითოთ შინაური ცხოველი."))
                    diagnosis = request.form.get("diagnosis")
                    treatment = request.form.get("treatment")
                    date = request.form.get("date")
                    if not date:
                        date = dt.today()
                    comment = request.form.get("comment")

                    try:
                        edit_mode = request.form.get("edit_mode")
                        if edit_mode:
                            visit_id = request.form.get("visit_id")
                            visit = Visit.get_visit(visit_id)
                            if visit:
                                visit.clinic_id = clinic
                                visit.vet_id = vet.vet_id
                                visit.owner_id = owner_id
                                try:
                                    visit.pet_id = pet_id
                                except Exception as e:
                                    logger.exception(
                                        f'{e.__class__.__name__} -> {e}')
                                    flash(
                                        _(
                                            "გთხოვთ მიუთითოთ შინაური ცხოველის "
                                            + "მფლობელი და შინაური ცხოველი."
                                        ),
                                        category="error",
                                    )
                                visit.diagnosis = diagnosis
                                visit.treatment = treatment
                                visit.date = date
                                visit.comment = comment
                                db.session.commit()
                                return redirect(
                                    url_for(
                                        "general_logic.vet_logic",
                                        action=1,
                                        choice=4,
                                    )
                                )

                    except Exception as e:
                        logger.warning(
                            f"Editmode is False or nonexistant -> {e}"
                        )

                    try:
                        visit = Visit(
                            clinic_id=clinic,
                            vet_id=vet.vet_id,
                            owner_id=owner_id,
                            pet_id=pet_id,
                            diagnosis=diagnosis,
                            treatment=treatment,
                            comment=comment,
                            date=date,
                        )
                        db.session.add(visit)
                        db.session.commit()
                    except Exception as e:
                        logger.exception(f'{e.__class__.__name__} -> {e}')

                elif request.method == "GET":
                    try:
                        # Querying PersonToClinic and getting clinics to work w
                        # Js catches data and responsively gives out options
                        my_clinics = (
                            db.session.query(PersonToClinic.clinic_id)
                            .filter_by(person_id=current_user.id)
                            .all()
                        )

                        clinic_ids = [
                            associacion.clinic_id
                            for associacion in my_clinics
                        ]

                        staff_members_by_c = {}
                        for clinic_id in clinic_ids:
                            # Query for staff members at this clinic
                            staff_members_query = (
                                db.session.query(Person)
                                .join(
                                    PersonToClinic,
                                    PersonToClinic.person_id == Person.id,
                                )
                                .filter(
                                    PersonToClinic.clinic_id == clinic_id,
                                    PersonToClinic.person_id
                                    != current_user.id,
                                )
                                .all()
                            )

                            # Add the staff members to the dictionary
                            staff_member_dicts = [
                                {
                                    "id": member.id,
                                    "name": member.name,
                                    "lastname": member.lastname,
                                    "phone": member.phone,
                                }
                                for member in staff_members_query
                            ]

                            # Add the list of dictionaries to the
                            # staff_members_by_clinic dictionary
                            staff_members_by_c[clinic_id] = staff_member_dicts

                        s_m_by_clinic = json.dumps(staff_members_by_c)
                        clinics = (
                            db.session.query(Clinic)
                            .filter(Clinic.clinic_id.in_(clinic_ids))
                            .all()
                        )

                        try:
                            visit_id = request.args.get("visit_id")
                            if visit_id:
                                visit = Visit.get_visit(visit_id)
                                if visit:
                                    return render_template(
                                        "login/vet.html",
                                        action=action,
                                        choice=choice,
                                        edit_mode=True,
                                        visit=visit,
                                        clinics=clinics,
                                        staff_members_by_clinic=s_m_by_clinic,
                                    )
                        except Exception as e:
                            logger.exception(f'{e.__class__.__name__} -> {e}')

                        return render_template(
                            "login/vet.html",
                            action=action,
                            choice=choice,
                            edit_mode=False,
                            clinics=clinics,
                            visit=None,
                            staff_members_by_clinic=s_m_by_clinic,
                        )

                    except Exception as e:
                        logger.exception(f'{e.__class__.__name__} -> {e}')
                    return render_template(
                        "login/vet.html",
                        action=action,
                        choice=choice,
                        clinics=None,
                        staff_members=None,
                    )

            elif action == 1:
                vet = Vet.get_vet(current_user.id)
                if vet:
                    visits = Visit.get_visits_by_vet(vet.vet_id)

                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        visits=visits,
                    )
                else:
                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        visits=None,
                    )

        case 5:  # Add my clinic
            if action == 0:
                vet_data = Vet.get_vet(current_user.id)
                if request.method == "POST":
                    clinic_name = request.form.get("clinic-name")
                    desc = request.form.get("comment")
                    coordinates = request.form.get("coordinates")
                    try:
                        edit_mode = request.form.get("edit_mode")
                        clinic_id = request.form.get("clinic_id")
                        clinic = Clinic.get_clinic(clinic_id)
                        if edit_mode:
                            if clinic:
                                clinic.clinic_name = clinic_name
                                clinic.desc = desc
                                clinic.coordinates = coordinates
                                db.session.commit()
                                return redirect(
                                    url_for(
                                        "general_logic.vet_logic",
                                        choice=choice,
                                        action=1,
                                    )
                                )
                    except Exception as e:
                        logger.warning(
                            f"Editmode is False or nonexistant -> {e}"
                        )
                    try:
                        clinic = Clinic(
                            clinic_name=clinic_name,
                            desc=desc,
                            coordinates=coordinates,
                        )
                        db.session.add(clinic)
                        db.session.commit()
                        clinic_id = clinic.clinic_id
                        # adding mixture
                        pc_associacion = PersonToClinic(
                            person_id=current_user.id,
                            clinic_id=clinic_id,
                            is_clinic_owner=True,
                        )
                        db.session.add(pc_associacion)
                        db.session.commit()
                        flash(
                            _("კლინიკა წარმატებით დაემატა"),
                            category="success",
                        )
                        return redirect(
                            url_for(
                                "general_logic.vet_logic",
                                choice=choice,
                                action=1,
                            )
                        )
                    except Exception as e:
                        flash(f"Unexpected Logic error: {e}")

                elif request.method == "GET":
                    if vet_data:
                        try:
                            clinic_id = request.args.get("clinic_id")
                            if clinic_id:
                                clinic = Clinic.get_clinic(clinic_id)
                                if clinic:
                                    return render_template(
                                        "login/vet.html",
                                        action=action,
                                        choice=choice,
                                        edit_mode=True,
                                        clinic=clinic,
                                        vet_data=vet_data,
                                    )

                        except Exception as e:
                            logger.exception(f'{e.__class__.__name__} -> {e}')
                        return render_template(
                            "login/vet.html",
                            action=action,
                            choice=choice,
                            edit_mode=False,
                            clinic=None,
                            vet_data=vet_data,
                        )
                    else:
                        return render_template(
                            "login/vet.html",
                            action=action,
                            choice=choice,
                            edit_mode=False,
                            clinic=None,
                            vet_data=None,
                        )

            elif action == 1:
                if request.method == "GET":
                    try:
                        # Query all associacions for the current user
                        person_clinic = PersonToClinic.get_clinic_with_person(
                            current_user.id
                        )

                        # Initialize data structures
                        clinics_info = []
                        for associacion in person_clinic:
                            # Query the clinic
                            clinic = Clinic.get_clinic(associacion.clinic_id)

                            if clinic:
                                # Query the owner of the clinic
                                owner = PersonToClinic.get_clinic_owner(
                                    clinic.clinic_id
                                )
                                # Query other personnel of the clinic
                                personnel = (
                                    db.session.query(Person)
                                    .join(PersonToClinic)
                                    .filter(
                                        PersonToClinic.clinic_id
                                        == clinic.clinic_id,
                                        PersonToClinic.is_clinic_owner
                                        is False,
                                        PersonToClinic.person_id
                                        != current_user.id,
                                    )
                                    .all()
                                )

                                if (
                                    isinstance(clinic.coordinates, str)
                                    and "," in clinic.coordinates
                                ):
                                    try:
                                        latitude_str, longitude_str = (
                                            clinic.coordinates.split(",")
                                        )
                                        latitude = float(latitude_str)
                                        longitude = float(longitude_str)
                                    except ValueError as e:
                                        logger.warning(
                                            "Invalid coordinates format "
                                            + "for clinic "
                                            + f"{clinic.clinic_name}: "
                                            + f"{clinic.coordinates} -> {e}"
                                        )
                                        continue
                                else:
                                    logger.warning(
                                        "No valid coordinates: "
                                        + f"{clinic.clinic_name}"
                                    )
                                    continue

                                # Structure data
                                clinic_data = {
                                    "clinic": clinic,
                                    "latitude": latitude,
                                    "longitude": longitude,
                                    "owner": owner,
                                    "personnel": personnel,
                                }

                                clinics_info.append(clinic_data)
                        vet_data = (
                            db.session.query(Vet)
                            .filter_by(person_id=current_user.id)
                            .one_or_none()
                        )
                        if vet_data:
                            return render_template(
                                "login/vet.html",
                                choice=choice,
                                action=action,
                                clinics_info=clinics_info,
                                vet_data=vet_data,
                            )
                        else:
                            return render_template(
                                "login/vet.html",
                                choice=choice,
                                action=action,
                                clinics_info=clinics_info,
                                vet_data=None,
                            )

                    except Exception as e:
                        logger.exception(f'{e.__class__.__name__} -> {e}')

            elif action == 2:
                if request.method == "POST":
                    clinic_id = request.form.get("clinic_id")
                    visibility = request.form.get("visibility")

                    if clinic_visibility_toggler(clinic_id, visibility):
                        return redirect(
                            url_for(
                                "general_logic.vet_logic",
                                choice=choice,
                                action=1,
                            )
                        )
                    else:
                        flash(_("პრობლემა... კლინიკის დამალვა ვერ მოხერხდა"))
                        return redirect(
                            url_for(
                                "general_logic.vet_logic",
                                choice=choice,
                                action=1,
                            )
                        )
                else:
                    return redirect(
                        url_for(
                            "general_logic.vet_logic", choice=choice, action=1
                        )
                    )

            elif action == 3:
                if request.method == "GET":
                    search_query = request.args.get("q", "").strip()
                    clinics_info = []
                    unique_associacions = db.session.query(
                        PersonToClinic
                    ).filter_by(is_clinic_owner=True)

                    # If there is a search query, filter the results
                    if search_query:
                        unique_associacions = unique_associacions.join(
                            Clinic
                        ).filter(
                            Clinic.clinic_name.like(f"%{search_query}%"),
                            Clinic.visibility is True,
                        )

                    unique_associacions = unique_associacions.all()

                    for associacion in unique_associacions:
                        # Query the clinic
                        clinic = Clinic.get_visible_clinic(
                            associacion.clinic_id
                        )

                        if clinic:
                            # Query the owner of the clinic
                            owner = PersonToClinic.get_clinic_owner(
                                clinic.clinic_id
                            )

                            if (
                                isinstance(clinic.coordinates, str)
                                and "," in clinic.coordinates
                            ):
                                try:
                                    latitude_str, longitude_str = (
                                        clinic.coordinates.split(",")
                                    )
                                    latitude = float(latitude_str)
                                    longitude = float(longitude_str)
                                except ValueError as e:
                                    logger.warning(
                                        "Invalid coordinates "
                                        + f"{clinic.clinic_name}:"
                                        + f" {clinic.coordinates} -> {e}"
                                    )
                                    continue
                            else:
                                logger.warning(
                                    "No valid coordinates  provided"
                                    + f" for clinic {clinic.clinic_name}"
                                )
                                # Skip this clinic and continue with the next
                                continue

                            # Structure data
                            clinic_data = {
                                "clinic": clinic,
                                "latitude": latitude,
                                "longitude": longitude,
                                "owner": owner,
                            }

                            clinics_info.append(clinic_data)

                    return render_template(
                        "login/vet.html",
                        choice=choice,
                        action=action,
                        clinics_info=clinics_info,
                    )

                # sending the request for clinic approval
                elif request.method == "POST":
                    clinic_id = request.form.get("clinic_id")
                    if clinic_id is not None:
                        clinic_id = int(clinic_id)

                        associacion = (
                            db.session.query(PersonToClinic)
                            .join(
                                Person, Person.id == PersonToClinic.person_id
                            )
                            .filter(
                                PersonToClinic.clinic_id == clinic_id,
                                PersonToClinic.is_clinic_owner is True,
                            )
                            .one_or_none()
                        )

                        if associacion:
                            send_request = Requests(
                                requester_id=current_user.id,
                                reciever_id=associacion.person_id,
                                request_type="clinic",
                                request_sent=dt.today(),
                                ref=clinic_id,
                            )
                            db.session.add(send_request)
                            try:
                                db.session.commit()
                                return redirect(
                                    url_for(
                                        "general_logic.vet_logic",
                                        choice=3,
                                        action=0,
                                    )
                                )
                            except Exception as e:
                                db.session.rollback()
                                logger.exception(
                                    f'{e.__class__.__name__} -> {e}')
                        else:
                            logger.debug("No associacion was found")
                            return render_template(
                                "login/vet.html", choice=8, action=0
                            )
                    else:
                        logger.debug("clinic_id is None or invalid")
                        return render_template(
                            "login/vet.html", choice=8, action=0
                        )

            elif action == 4:
                if request.method == "POST":
                    clinic_id = request.form.get("clinic_id")
                    clinic_owner = None

                    if clinic_id:
                        staffs = (
                            db.session.query(PersonToClinic, Person)
                            .join(
                                Person, Person.id == PersonToClinic.person_id
                            )
                            .filter(PersonToClinic.clinic_id == clinic_id)
                            .all()
                        )
                        if staffs:
                            # Find the clinic owner among the staff
                            for staff, person in staffs:
                                if (
                                    staff.is_clinic_owner
                                    and person.id == current_user.id
                                ):
                                    clinic_owner = person.id
                                    break

                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            staffs=staffs,
                            clinic_owner=clinic_owner,
                        )
                    else:
                        return render_template(
                            "login/vet.html",
                            choice=choice,
                            action=action,
                            staffs=None,
                            clinic_owner=None,
                        )

            else:
                abort(404)

        case 8:  # My Data
            if request.method == "POST":
                firstname = request.form.get("firstname")
                lastname = request.form.get("lastname")
                address = request.form.get("address")
                changed = change_user_data(firstname, lastname, address)
                if changed:
                    flash(
                        _("მონაცემები წარმატებით შეიცვალა."),
                        category="success",
                    )
                return render_template(
                    "login/vet.html", choice=choice, action=action
                )

    return render_template("login/vet.html", choice=choice)


# Addition functions section


def register_pet(
    pet_name, pet_species, pet_breed, recent_vaccination, gender, birth_date
):
    try:
        owner = Owner.get_owner(current_user.id)
        if owner is None:
            owner = Owner(person_id=current_user.id)
            db.session.add(owner)
            db.session.commit()
        if owner is not None:
            breed = PetBreed.get_breed(pet_breed)
            pet = Pet(
                owner_id=owner.owner_id,
                name=pet_name,
                pet_species=pet_species,
                pet_breed=breed.breed_id,
                recent_vaccination=(
                    recent_vaccination if recent_vaccination else None
                ),  # Ternary Shorcircuiting
                gender=gender,
                birth_date=birth_date,
            )
            db.session.add(pet)
            db.session.commit()
            return True
    except Exception as e:
        flash(f"{e}")


@general_logic.route("/add_new_note", methods=["POST"])
@grant_access([2])
def add_note():
    # category = request.form.get('icon_option')
    note = request.form.get("note")
    person_id = current_user.id
    created = dt.today()
    new_note = Note(person_id=person_id, created=created, content=note)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("general_logic.admin_logic", choice=2, action=0))


# Getting data functions section


@general_logic.route("/get_pet_breeds", methods=["POST"])
def get_pet_breeds():
    # Get the selected species_id from the frontend
    species_id = request.json["species_id"]

    # Retrieve the pet breeds for the selected species_id
    pet_breeds = PetBreed.get_breeds_by_species(species_id)

    # Prepare a list of breed names to send to the frontend
    breed_list = [breed.breed for breed in pet_breeds]

    return jsonify(breed_list)


# Editing functions section


@general_logic.route(
    "edit/<int:action>/<int:pet_id>", methods=["GET", "POST"]
)
@login_required
def edit_pet(action, pet_id):
    pet = Pet.get_pet(pet_id)
    changed = False
    if pet:
        if request.method == "POST":
            name = request.form.get("name")
            # species = request.form.get('species')
            # breed = request.form.get('breed')
            recent_vaccination = request.form.get("recent_vaccination")
            if name is not None and name != "":
                pet.name = name
                db.session.commit()
                changed = True

            if recent_vaccination is not None and recent_vaccination != "":
                pet.recent_vaccination = recent_vaccination
                db.session.commit()
                changed = True
            if changed:
                flash(_("მონაცემები წარმატებით შეიცვალა"), category="success")
            if current_user.user_type == 1:
                return redirect(
                    url_for("general_logic.owner_logic", action=1)
                )
            elif current_user.user_type == 2:
                return redirect(
                    url_for("general_logic.admin_logic", choice=1, action=1)
                )
            elif current_user.user_type == 3:
                return redirect(
                    url_for("general_logic.vet_logic", choice=1, action=1)
                )

    return redirect(url_for("general_logic.owner_logic", action=action))


@general_logic.route(
    "/admin/edit_user/<int:choice>/<int:person_id>", methods=["GET", "POST"]
)
@login_required
@grant_access([2])
def edit_user(person_id, choice):
    """
    Edits user data based on the given person_id and user_type.

    Parameters:
    person_id (int): The id of the user to be edited.
    choice (int): The choice variable for appropriate action.

    Returns:
    redirect: Redirects to the appropriate panel with the updated user data.
    """
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        mail = request.form.get("mail")
        user_type = request.form.get("user_type")
        address = request.form.get("address")
        phone = request.form.get("phone")

        choice == 0

        person = Person.get_person(person_id)
        if person:

            previous_person_type = person.user_type
            person.name = name
            person.lastname = lastname
            person.mail = mail
            person.user_type = user_type
            person.address = address
            person.phone = phone

            db.session.commit()
            if int(user_type) == 1:  # Regular user
                if previous_person_type == 2:
                    admin = Admin.get_admin(person_id)
                    if admin:
                        admin.active = False

                # Sets previous role's active status to False (Vet and Editor)
                if previous_person_type == 3:
                    vet = Vet.get_vet(person_id)
                    if vet:
                        vet.active = False

                if previous_person_type == 4:
                    editor = Editor.get_editor(person_id)
                    if editor:
                        editor.active = False

            if int(user_type) == 2:  # Admin
                admin = Admin.get_admin(person_id)
                if admin:
                    admin.active = True
                else:
                    admin = Admin(person_id=person_id, active=True)
                    db.session.add(admin)

                # Sets previous role's active status to False (Vet and Editor)
                if previous_person_type == 3:
                    vet = Vet.get_vet(person_id)
                    if vet:
                        vet.active = False
                if previous_person_type == 4:
                    editor = Editor.get_editor(person_id)
                    if editor:
                        editor.active = False

            elif int(user_type) == 3:  # Vet
                vet = Vet.get_vet(person_id)
                if vet:
                    li = request.form.get("license")
                    if li:
                        vet.has_license = bool(li)
                else:
                    vet = Vet(person_id=person_id, active=True)
                    db.session.add(vet)

                # Set previous role's active statuses to False
                if previous_person_type == 2:
                    admin = Admin.get_admin(person_id)
                    if admin:
                        admin.active = False

                if previous_person_type == 4:
                    editor = Editor.get_editor(person_id)
                    if editor:
                        editor.active = False

            elif int(user_type) == 4:  # Editor
                editor = Editor.get_editor(person_id)
                if editor:
                    editor.active = True
                else:
                    editor = Editor(person_id=person_id, active=True)
                    db.session.add(editor)

                # Set previous role's active status to False (Vet)
                if previous_person_type == 2:
                    admin = Admin.get_admin(person_id)
                    if admin:
                        admin.active = False

                if previous_person_type == 3:
                    vet = Vet.get_vet(person_id)
                    if vet:
                        vet.active = False

            db.session.commit()

        else:
            flash(_("მომხმარებელი ვერ მოიძებნა."), category="error")
        action = request.form.get("action")
        if action:
            action = int(action)
        else:
            action = 0
        return redirect(
            url_for("general_logic.admin_logic", choice=choice, action=action)
        )


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


@general_logic.route("edit/<int:action>/<int:note_id>", methods=["POST"])
@login_required
def edit_note(note_id):
    note = Note.get_note_by_id(note_id)
    new_note = request.form.get("comment")
    note.note = new_note
    try:
        db.session.commit()
    except Exception as e:
        logger.exception(f'{e.__class__.__name__} -> {e}')
        db.session.rollback()
        flash(_("შეცდომა."), category="error")
    return redirect(url_for("general_logic.admin_logic", choice=2, action=0))


@general_logic.route(
    "give_leadership/<int:clinic_id>/<int:person_id>",
    methods=["GET", "POST"],
)
@login_required
@grant_access([3])
def give_clinic_ownership(clinic_id, person_id):
    """
    This function is used to give ownership of a clinic to another vet.

    Parameters:
    clinic_id (int): The id of the clinic to be transferred.
    person_id (int): The id of the vet who will be given ownership.

    Returns:
    Redirects to the vet panel after the ownership transfer.
    """

    if person_id == current_user.id:
        flash(
            _("თქვენ უკვე ხართ მოცემული კლინიკის მფლობელი"), category="error"
        )
        return redirect(
            url_for("general_logic.vet_logic", choice=5, action=1)
        )
    current_owner = (
        db.session.query(PersonToClinic)
        .filter_by(
            clinic_id=clinic_id,
            person_id=current_user.id,
            is_clinic_owner=True,
        )
        .one_or_none()
    )
    if current_owner:
        new_owner = (
            db.session.query(PersonToClinic)
            .filter_by(
                clinic_id=clinic_id,
                person_id=person_id,
                is_clinic_owner=False,
            )
            .one_or_none()
        )
        if new_owner:
            vet_data = Vet.get_vet(person_id)
            if vet_data:
                vet_data.has_license = True
                vet_data.temporary_license = True  # maybe for later
                current_owner.is_clinic_owner = False
                new_owner.is_clinic_owner = True
                db.session.commit()
                flash("წარმატება")
    return redirect(url_for("general_logic.vet_logic", choice=5, action=1))


# clinic requests are controlled here
@general_logic.route(
    "request_control/<int:action>/<int:request_id>", methods=["GET", "POST"]
)
@login_required
@grant_access([3])
def clinic_request_control(action, request_id):
    request_data = Requests.get_request_by_id(request_id)
    if request_data:
        match action:
            case 0:  # delete
                db.session.delete(request_data)
                db.session.commit()
                return redirect(
                    url_for("general_logic.vet_logic", choice=3, action=action)
                )
            case 1:  # approve
                legit = (
                    db.session.query(Vet)
                    .filter_by(
                        person_id=request_data.reciever_id, has_license=True
                    )
                    .one_or_none()
                )
                if legit:
                    clinic_data = Clinic.get_clinic(request_data.ref)
                    if clinic_data:
                        check_associacion = (
                            db.session.query(PersonToClinic)
                            .filter_by(
                                person_id=request_data.requester_id,
                                clinic_id=clinic_data.clinic_id,
                            )
                            .one_or_none()
                        )

                        if check_associacion is None:
                            new_associacion = PersonToClinic(
                                person_id=request_data.requester_id,
                                clinic_id=clinic_data.clinic_id,
                                is_clinic_owner=False,
                            )
                            request_data.approved = True
                            db.session.add(new_associacion)
                            db.session.commit()
                        else:
                            flash(
                                _(
                                    "თქვენ უკვე გაწევრიანებული ხართ"
                                    + " მოცემულ კლინიკაში"
                                ),
                                category="error",
                            )
                            db.session.delete(request_data)
                            db.session.commit()
                    return redirect(
                        url_for(
                            "general_logic.vet_logic", choice=3, action=action
                        )
                    )
                else:
                    abort(404)
            case 2:  # deny
                legit = (
                    db.session.query(Vet)
                    .filter_by(
                        person_id=request_data.reciever_id, has_license=True
                    )
                    .one_or_none()
                )
                if legit:
                    try:
                        request_data.approved = None
                        db.session.commit()
                        clinic_data = Clinic.get_clinic(request_data.ref)
                        if clinic_data:
                            check_associacion = (
                                db.session.query(PersonToClinic)
                                .filter_by(
                                    person_id=request_data.requester_id,
                                    clinic_id=clinic_data.clinic_id,
                                )
                                .one_or_none()
                            )
                            if check_associacion:
                                db.session.delete(check_associacion)
                                db.session.commit()
                    except Exception as e:
                        logger.exception(f'{e.__class__.__name__} -> {e}')

                    return redirect(
                        url_for(
                            "general_logic.vet_logic", choice=3, action=action
                        )
                    )
                else:
                    abort(404)
            case _:
                abort(404)
    else:
        return redirect(
            url_for("general_logic.vet_logic", choice=3, action=action)
        )


# Removing functions section


@general_logic.route(
    "/remove_pet/<int:action>/<int:pet_id>", methods=["GET", "DELETE"]
)
@login_required
def remove_pet(action, pet_id):
    pet = Pet.get_pet(pet_id)
    history = PetHistory.get_history_by_pet(pet_id)
    if pet is not None:
        owner = Owner.get_owner(current_user.id)
        if owner is not None:
            try:
                if history:
                    for h in history:
                        db.session.delete(h)
                db.session.delete(pet)
                db.session.commit()

                remaining_pets = Pet.get_pets(owner.owner_id)
                if not remaining_pets:
                    db.session.delete(owner)
                    db.session.commit()

            except Exception as e:
                logger.exception(f'{e.__class__.__name__} -> {e}')
        if current_user.user_type == 1:
            return redirect(url_for("general_logic.owner_logic", action=1))
        elif current_user.user_type == 2:
            return redirect(
                url_for("general_logic.admin_logic", choice=1, action=1)
            )
        elif current_user.user_type == 3:
            return redirect(
                url_for("general_logic.vet_logic", choice=1, action=1)
            )
    else:
        abort(404)


@general_logic.route(
    "/remove_history/<int:history_id>", methods=["GET", "DELETE"]
)
@login_required
def remove_history(history_id):
    pet_history = PetHistory.get_history(history_id)
    if pet_history:
        db.session.delete(pet_history)
        db.session.commit()
        if current_user.user_type == 1:
            return redirect(url_for("general_logic.owner_logic", action=2))
        if current_user.user_type == 2:
            return redirect(
                url_for("general_logic.admin_logic", choice=1, action=2)
            )
        else:
            abort(404)


@general_logic.route("/remove_note/<int:note_id>", methods=["GET", "DELETE"])
@login_required
@grant_access([2])
def remove_note(note_id):
    admin_note = Note.get_note_by_id(note_id)
    if admin_note:
        db.session.delete(admin_note)
        db.session.commit()
        return redirect(
            url_for("general_logic.admin_logic", choice=2, action=0)
        )

    else:
        return redirect(
            url_for("general_logic.admin_logic", choice=2, action=0)
        )


@general_logic.route(
    "/remove_visit/<int:visit_id>", methods=["GET", "DELETE"]
)
@login_required
@grant_access([3])
def remove_visit(visit_id):
    visit = Visit.get_visit(visit_id)
    if visit:
        db.session.delete(visit)
        db.session.commit()
        return redirect(
            url_for("general_logic.vet_logic", choice=4, action=1)
        )

    else:
        return redirect(
            url_for("general_logic.vet_logic", choice=4, action=1)
        )


@general_logic.route(
    "/remove_staff/<int:associacion_id>", methods=["GET", "DELETE"]
)
@login_required
@grant_access([3])
def remove_staff(associacion_id):
    associacion = PersonToClinic.get_bridge(associacion_id)
    if associacion:
        db.session.delete(associacion)
        db.session.commit()
        return redirect(
            url_for("general_logic.vet_logic", choice=5, action=4)
        )

    else:
        return redirect(
            url_for("general_logic.vet_logic", choice=5, action=4)
        )


# requests
def get_clinic_by_request(requests):
    connections = []
    for req in requests:
        clinic_id = req.ref
        clinic = Clinic.get_clinic(clinic_id)
        if clinic:
            connection = {"request": req, "clinic": clinic}
            connections.append(connection)
    return connections


def clinic_visibility_toggler(clinic_id, visibility):
    """
    Toggles the visibility of a clinic based on the given visibility status.

    Parameters:
    clinic_id (int): The id of the clinic to be toggled.
    visibility (str): The visibility status to be set.
                      It can be either "True" or "False".

    Returns:
    bool: True if the visibility status is successfully
          toggled, False otherwise.

    Raises:
    Exception: If any error occurs during the database operation.
    """
    try:
        # Retrieve clinic by clinic_id
        clinic = Clinic.get_clinic(clinic_id)

        if clinic:
            # Toggle the visibility
            if visibility == "False":
                clinic.visibility = True
            if visibility == "True":
                clinic.visibility = False

            db.session.commit()

            return True
        else:
            logger.debug(f"No clinic found with id {clinic_id}")
            return False
    except Exception as e:
        logger.exception(
            f"Failed to toggle visibility for clinic {clinic_id}: {e}"
        )
        return False
