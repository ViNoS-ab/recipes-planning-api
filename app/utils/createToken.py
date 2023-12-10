import jwt
from datetime import datetime, timedelta
import os


def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(
        payload,
        os.environ.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
    except:
        return 'Invalid token. Please log in again.'