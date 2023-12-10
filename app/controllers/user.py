from app.utils.classToDict import classToArrayOfDicts , classToDict

def getUsersRoute(db , Users):
  users = db.session.execute(db.select(Users).order_by(Users.username)).scalars().all()
  res = classToArrayOfDicts(users)
  return jsonify(res)