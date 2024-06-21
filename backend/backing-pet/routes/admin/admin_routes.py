@blp.route("/person/<int:person_id>")
class PersonExtendedRoutes(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, PersonGetterSchema)
    def get(self, person_id):
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person not found")
        return jsonify(person.to_dict())

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PersonUpdateSchema)
    @blp.response(200, PersonGetterSchema)
    def put(self, person_id, user_data):
        person = Person.query.filter_by(id=person_id).first()
        if not person:
            abort(404, message="Person not found")
        person.name = user_data["name"]
        person.lastname = user_data["lastname"]
        person.phone = user_data["phone"]
        person.address = user_data["address"]
        person.user_type = user_data["user_type"]
        person.confirmed = user_data["confirmed"]
        try:
            db.session.commit()
            return {"message": "successfully edited user data", **user_data}
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(
                500,
                message="While editing user data, "
                + "unexpected error occured",
            )
