from app.utils.classToDict import classToArrayOfDicts , classToDict
from flask import jsonify

def getUsersRoute(db , Users):
  try:
    users = db.session.execute(db.select(Users).order_by(Users.username)).scalars().all()
    if len(users) == 0 :
      return jsonify({'success': False ,  'messsage': 'there are no users'}) , 404
    res = classToArrayOfDicts(users)
    return jsonify(res), 200
  except Exception as e: 
    return jsonify({'success': False ,  'messsage': 'there was an error getting all users'}) , 500

def getMe(user):
  return jsonify({'user': classToDict(user)  , 'success': True}) , 200
