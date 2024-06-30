from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import UserRequests, Vet, PersonClinic
from validators.request_schema import (
    RequestSchema,
    ApprovealRequestSchema,
    ClinicRequestSchema,
    PlainRequestSchema,
    ClinicApprovalRequestSchema,
)
from logs import logger_config

logger = logger_config.logger

blp = Blueprint(
    "Requests",
    __name__,
    description="User Request operations",
    url_prefix="/requests",
)


@blp.route("/send/licence_approval")
class SendApproval(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, RequestSchema)
    def get(self):
        requests = UserRequests.query.filter_by(
            request_type="Licence Approval",
            requester_id=current_user.id,
        ).all()
        if not requests:
            abort(404, message="No pending licence approval request found")
        return jsonify([req.to_dict() for req in requests])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(RequestSchema)
    def post(self, request_data):
        if current_user.user_type == 3:
            new_request = UserRequests(**request_data)
            new_request.requester_id = current_user.id
            new_request.request_type = "Licence Approval"
            try:
                db.session.add(new_request)
                db.session.commit()
                return jsonify(new_request.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while creating a new request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while creating a new request",
                )
        abort(400, message="Requester is not a Vet")

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self, request_id):
        if current_user.user_type == 3:
            request = UserRequests.query.filter_by(
                request_id=request_id
            ).first()
            if not request:
                abort(404, message="Request not found")
            if request.requester_id != current_user.id:
                abort(
                    403,
                    message="You are not authorized to delete this request",
                )
            try:
                db.session.delete(request)
                db.session.commit()
                return (
                    jsonify({"message": "Request deleted successfully"}),
                    200,
                )
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"An error occurred while deleting request: {e}")
                abort(
                    500,
                    message="An error occurred while deleting request",
                )
        abort(400, message="Requester is not a Vet")


@blp.route("/recieved/licence_approval")
class ReceivedApproval(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, RequestSchema)
    def get(self):
        requests = UserRequests.query.filter_by(
            request_type="Licence Approval",
            receiver_id=current_user.id,
        ).all()
        if not requests:
            abort(404, message="No received licence approval request found")
        return jsonify(
            [req.to_dict() for req in requests if req.ban is False]
        )

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ApprovealRequestSchema)
    @blp.response(200, RequestSchema)
    def post(self, request_data):
        user_request = UserRequests.query.filter_by(
            request_id=request_data["request_id"]
        ).first()
        if not user_request:
            abort(404, message="Request not found")
        if user_request.receiver_id != current_user.id:
            abort(
                403,
                message="You are not authorized " + "to approve this request",
            )
        if request_data.get("approved"):
            user_request.approved = True
            vet = Vet.query.filter_by(
                person_id=user_request.requester_id
            ).first()
            if vet and vet.active:
                vet.has_license = True
            else:
                abort(400, "Requester is not a Vet")
            try:
                db.session.commit()
                return jsonify(user_request.to_dict())
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while approving request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while approving request",
                )
        if (
            request_data.get("approved") is False
            and current_user.user_type == 2
        ):
            user_request.ban = True
            return jsonify(user_request.to_dict())


@blp.route("/send/clinic_join")
class SendClinicJoin(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, ClinicRequestSchema)
    def get(self):
        requests = UserRequests.query.filter_by(
            request_type="Clinic Join",
            requester_id=current_user.id,
        ).all()
        if not requests:
            abort(404, message="No pending clinic join request found")
        return jsonify([req.to_dict() for req in requests])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ClinicRequestSchema)
    def post(self, request_data):
        if current_user.user_type == 3:
            new_request = UserRequests(**request_data)
            new_request.requester_id = current_user.id
            licenced_vet = Vet.query.filter_by(
                person_id=request_data["reciever_id"], has_licence=True
            ).first()
            if not licenced_vet:
                abort("Reciever Veterinarian is not licenced")
            new_request.request_type = "Clinic Join"
            try:
                db.session.add(new_request)
                db.session.commit()
                return jsonify(new_request.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while creating a new request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while creating a new request",
                )
        abort(400, message="Requester is not a Vet")

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PlainRequestSchema)
    def delete(self, data):
        if current_user.user_type == 3:
            request = UserRequests.query.filter_by(
                request_id=data["request_id"]
            ).first()
            if not request:
                abort(404, message="Request not found")
            if request.requester_id != current_user.id:
                abort(
                    403,
                    message="You are not authorized to delete this request",
                )
            try:
                db.session.delete(request)
                db.session.commit()
                return (
                    jsonify({"message": "Request deleted successfully"}),
                    200,
                )
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"An error occurred while deleting request: {e}")
                abort(
                    500,
                    message="An error occurred while deleting request",
                )
        abort(
            400, message="Requester is not authorized to delete this request"
        )


@blp.route("/send/clinic_leave")
class SendClinicLeave(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, ClinicRequestSchema)
    def get(self):
        requests = UserRequests.query.filter_by(
            request_type="Clinic Leave",
            requester_id=current_user.id,
        ).all()
        if not requests:
            abort(404, message="No pending clinic leave request found")
        return jsonify([req.to_dict() for req in requests])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ClinicRequestSchema)
    def post(self, request_data):
        if current_user.user_type == 3:
            licenced_vet = Vet.query.filter_by(
                person_id=request_data["reciever_id"], has_licence=True
            ).first()
            if not licenced_vet:
                abort("Reciever Veterinarian is not licenced")
            new_request = UserRequests(**request_data)
            new_request.requester_id = current_user.id
            new_request.request_type = "Clinic Leave"
            try:
                db.session.add(new_request)
                db.session.commit()
                return jsonify(new_request.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while creating a new request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while creating a new request",
                )
        abort(400, message="Requester is not a Vet")

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PlainRequestSchema)
    def delete(self, data):
        if current_user.user_type == 3:
            request = UserRequests.query.filter_by(
                request_id=data["request_id"], requester_id=current_user.id
            ).first()
            if not request:
                abort(404, message="Request not found")
            try:
                db.session.delete(request)
                db.session.commit()
                return (
                    jsonify({"message": "Request deleted successfully"}),
                    200,
                )
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"An error occurred while deleting request: {e}")
                abort(
                    500,
                    message="An error occurred while deleting request",
                )
        abort(400, message="Requester is not authorized to delete this")


@blp.route("/recieve/clinic_join")
class RecieveClinicJoin(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.response(200, ClinicRequestSchema)
    def get(self):
        requests = UserRequests.query.filter_by(
            request_type="Clinic Join",
            receiver_id=current_user.id,
        ).all()
        if not requests:
            abort(404, message="No pending clinic join request found")
        return jsonify([req.to_dict() for req in requests])

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(ClinicApprovalRequestSchema)
    def post(self, request_data):
        request = UserRequests.query.filter_by(
            request_id=request_data["request_id"]
        ).first()
        if not request:
            abort(404, message="Request not found")
        if request.receiver_id != current_user.id:
            abort(
                403,
                message="You are not authorized to approve this request",
            )
        if request_data["approved"]:
            request.approved = request_data.get("approved", False)
            try:
                new_member = PersonClinic(
                    person_id=request.requester_id,
                    clinic_id=request.reference_id,
                )
                db.session.add(new_member)
                db.session.commit()
                return jsonify(request.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while approving request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while approving request",
                )
        else:
            request.ban = True
            try:
                db.session.commit()
                return jsonify(request.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(
                    f"An error occurred while declining request: {e}"
                )
                abort(
                    500,
                    message="An error occurred while declining request",
                )

    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    @blp.arguments(PlainRequestSchema)
    def delete(self, data):
        request = UserRequests.query.filter_by(
            request_id=data["request_id"]
        ).first()
        if not request:
            abort(404, message="Request not found")
        if request.receiver_id != current_user.id:
            abort(
                403,
                message="You are not authorized to delete this request",
            )
        try:
            db.session.delete(request)
            db.session.commit()
            return (
                jsonify({"message": "Request deleted successfully"}),
                200,
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"An error occurred while deleting request: {e}")
            abort(
                500,
                message="An error occurred while deleting request",
            )


@blp.route("/clean")
class CleanRequests(MethodView):
    @jwt_required()
    @blp.doc(security=[{"JWT Auth": []}])
    def delete(self):
        banned_requests = UserRequests.query.filter_by(ban=True).all()
        for request in banned_requests:
            db.session.delete(request)
        try:
            db.session.commit()
            return jsonify({"message": "All banned requests deleted"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(
                f"An error occurred while deleting banned requests: {e}"
            )
            abort(
                500,
                message="An error occurred while deleting banned requests",
            )
