from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
)
from logs import logger_config

logger = logger_config.logger


blp = Blueprint(
    "Token", __name__, description="Token operations", url_prefix="/auth"
)


@blp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@blp.doc(security=[{"JWT Auth": []}])
def refresh():
    """
    Refresh JWT access token.

    This endpoint is used to refresh an expired
    JWT access token using a valid refresh token.
    The refresh token is required to authenticate
    the user and obtain a new access token.

    Parameters:
    refresh_token

    Returns:
    dict: A JSON response containing the new access token.

    Raises:
    401 if not authorized or refresh_token is invalid
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(
        access_token=access_token,
        refresh_token=request.headers.get("Authorization").split(" ")[1])
