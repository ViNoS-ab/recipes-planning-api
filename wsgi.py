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


if __name__ == "__main__":
    app.run(debug=True ,  port=8081 , host="0.0.0.0" , use_reloader=True)
    