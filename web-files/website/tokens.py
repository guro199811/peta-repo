from itsdangerous import URLSafeTimedSerializer

# Create a serializer with a secret key
serializer = None  # Define serializer outside the functions

def init_serializer(current_app):
    global serializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_confirmation_token(email, current_app):
    if serializer is None:
        init_serializer(current_app)
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    if serializer is None:
        init_serializer()
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
        return email
    except:
        return None
