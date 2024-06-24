from flask import jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
)


blp = Blueprint("Token", __name__, description="Token operations")


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
    None

    Returns:
    dict: A JSON response containing the new access token.

    Raises:
    None
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
