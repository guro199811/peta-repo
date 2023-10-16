from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# Create a serializer with a secret key
serializer = None  # Define serializer outside the functions

def init_serializer(current_app):
    global serializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_confirmation_token(email, current_app):
    if serializer is None:
        init_serializer(current_app)
    return serializer.dumps(email, salt='email-confirm')



