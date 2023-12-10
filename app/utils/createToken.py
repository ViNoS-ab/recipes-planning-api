import jwt
from datetime import datetime, timedelta
import os

MAX_AGE= 60 *60 *24

def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=MAX_AGE),
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