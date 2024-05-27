# Tokens section, used for generating serializers

from itsdangerous import URLSafeTimedSerializer

# Create a serializer with a secret key
# Define serializer outside the functions


def init_serializer(current_app):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer


def generate_token(email, current_app, salt):
    if 'serializer' not in globals():
        serializer = None   
    if serializer is None:
        serializer = init_serializer(current_app)
    return serializer.dumps(email, salt)
