from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy
from app.utils.classToDict import classToArrayOfDicts , classToDict
from app.models import User , RefreshToken , Recipe , Ingrediant , Planning , PlanningRecipe
from datetime import datetime, timedelta
import bcrypt
import jwt
from dot import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/v1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)


# importing Models and exporting them
Users = User.UsersModel(db)
RefreshTokens = RefreshToken.RefreshTokensModel(db)
Recipes = Recipe.RecipesModel(db)
Ingredients = Ingrediant.IngredientsModel(db)
Plannings = Planning.PlanningsModel(db)
PlanningRecipes = PlanningRecipe.PlanningRecipesModel(db)

# db.init_app(app)
token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "welcome to recipes-app api"


@app.get('/users')
def getUsers():
  users = db.session.execute(db.select(Users).order_by(Users.username)).scalars().all()
  res = classToArrayOfDicts(users)
  return jsonify(res)

salt = bcrypt.gensalt() 

@app.post('/signup')
def create():
    try:
        data = request.get_json()
        exists = db.session.execute(db.select(Users).filter_by(email=data['email'])).first()
        print(exists)
        if exists:
            res = {'message': 'user already exists', 'success': False}
            return (jsonify(res) , 400)
    
        bytes = data['password'].encode('utf-8') 
        hash = bcrypt.hashpw(bytes, salt) 
        user = Users(username=data['username'] , password=hash , email=data['email']    )
        db.session.add(user)
        db.session.commit()
        res = {'user': data, 'success': True}
        return (jsonify(res) , 200)

    except Exception as e:
        print(e)
        return (jsonify({'success': False , 'message': 'there was an error signing up try again later'}) , 500)

@app.post('/login')
def login():
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
        
        res = {'user': classToDict(user) , 'success': True}
        return (jsonify(res) , 200)
        
    except Exception as e:
        print(f"error in login : type of error : {type(e)} \n error : {e}  ")
        return (jsonify({'success': False , 'message': 'there was an error signing up try again later'}) , 500)


if __name__ == "__main__":
    app.run(debug=True ,  port=8081 , host="0.0.0.0" , use_reloader=True)
    