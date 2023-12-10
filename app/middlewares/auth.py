from functools import wraps
from flask import request , jsonify
import os
import jwt

def authunticated(db , User):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            # return 401 if token is not passed
            if not token:
                return jsonify({'message' : 'Token is missing !!' , 'success': False}), 401
            try:
                data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms="HS256")
                current_user = db.session.query(User).filter(User.id==data['sub']).first()
            except Exception as e:
                print(e)
                return jsonify({
                    'message' : 'Token is invalid !!' , 'success': False
                }), 401
            # returns the current logged in users context to the routes
            return  f(current_user, *args, **kwargs)
    
        return decorated
    return token_required

def is_admin(f):
    @wraps(f)
    def decorated(user ,*args , **kwargs):
            if user.role is not "admin":
                return jsonify({'success': False , 'message': "you don't have permission to make this action" }) , 403
            return f(user , *args , **kwargs)
    return decorated
