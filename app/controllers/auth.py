from flask import jsonify , request , make_response
from app.utils.createToken import generate_token , MAX_AGE
from app.utils.classToDict import classToArrayOfDicts , classToDict
import bcrypt
import jwt


def signup(db , Users):
    try:
        data = request.get_json()
        exists = db.session.execute(db.select(Users).filter_by(email=data['email'])).first()
        print(exists)
        if exists:
            res = {'message': 'user already exists', 'success': False}
            return (jsonify(res) , 400)
    
        bytes = data['password'].encode('utf-8') 
        salt = bcrypt.gensalt() 
        hash = bcrypt.hashpw(bytes, salt) 
        user = Users(username=data['username'] , password=hash , email=data['email'] , role=data['role']   )
        db.session.add(user)
        resObj = {'user': classToDict(user) , 'success': True}
        db.session.commit()
        resObj['user']['id'] = user.id
        res = make_response(jsonify(resObj))
        token = generate_token(user.id)
        res.set_cookie('htua' , token , max_age=MAX_AGE )
        return (res , 200)

    except Exception as e:
        print(e)
        return (jsonify({'success': False , 'message': 'there was an error signing up try again later'}) , 500)

def login(db, Users):
    try:
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            return (jsonify({'success': False , 'message': 'email and password are required'}) , 400)
        user = db.session.query(Users).filter_by(email=data['email']).first()
        
        if user is None:
            return ( jsonify({'success': False , 'message': 'this user does not exist'}), 404)
        match = bcrypt.checkpw(data['password'].encode('utf-8'), user.password)
        if not match:
            return ( jsonify({'success': False , 'message': 'wrong password'})  , 400)
        token = generate_token(user.id)
        resObj = {'user': classToDict(user) , 'success': True}
        res = make_response(jsonify(resObj))
        res.set_cookie('htua' , token , max_age=MAX_AGE, httponly=True )
        return (res , 200)
        
    except Exception as e:
        print(f"error in login : type of error : {type(e)} \n error : {e}  ")
        return (jsonify({'success': False , 'message': 'there was an error signing up try again later'}) , 500)

def logoutRoute () :
    res = make_response(jsonify({'success': True , 'message': 'user logged ouy succefully'}))
    res.set_cookie('htua' , '' , max_age=0 )
    return (res , 200)