# Does not work as Expected!!! Postproned its integration

from flask_jwt_extended import current_user
from functools import wraps
from typing import List
from types import MethodType


def grant_access(*user_types: List[int]):
    """
    Decorator function to grant access to certain user types.
    Intended to be used on router class methods...

    Parameters:
    *user_types List[int]: Variable length argument list of user types.

    1: User
    2: Admin
    3: Vet
    4: Editor

    Returns:
    METHOD: -> The decorated method if the current user's
                type is in the provided user types.
              -> Otherwise, it returns a dictionary with an
                access denied message.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.user_type in user_types:
                mthd = MethodType(func(*args, **kwargs), type(func))
                return mthd
            return {"message": "Access denied"}

        return wrapper

    return decorator
