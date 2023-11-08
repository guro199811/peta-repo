from flask import (Blueprint, render_template,
                request, jsonify)
from flask_login import login_required, current_user

from .views import grant_access
from . import db
from .models import *
import logging

ajax_logic = Blueprint('ajax_logic', __name__)

@grant_access([2, 3])
@ajax_logic.route('/search_owner', methods=['POST'])
def search_owner():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_input = request.form['searchInput']
        person = None
        if search_input.isdigit():
            person = db.session.query(Person).filter_by(id=int(search_input)).one_or_none()
        else:
            person = db.session.query(Person).filter_by(mail=search_input).one_or_none()

        if person:
            owner = db.session.query(Owner).filter_by(person_id = person.id).one_or_none()
            if owner:
                pets = db.session.query(Pet).filter_by(owner_id = owner.owner_id).all()
                pets_mixture = []
                for pet in pets:
                    pets_mixture.append(pet)
            else:
                pets_mixture = None
            # Return a snippet of HTML with the owner details
            
            owner_html = render_template('ajax_requests/owner_search_result.html', owner=owner, person = person, pets = pets_mixture)
            return jsonify(html=owner_html)
        else:
            # Return an error message
            return jsonify(html="<p>No owner found with the provided ID or Email.</p>")
