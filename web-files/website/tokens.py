from itsdangerous import URLSafeTimedSerializer
from ..main import app 

# Create a serializer with a secret key
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_confirmation_token(email):
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):  # Expiration in seconds
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
        return email
    except:
        return None