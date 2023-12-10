from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from app.models import User , RefreshToken , Recipe , Ingrediant , Planning , PlanningRecipe ,Tag
from dotenv import load_dotenv
import os
from app.middlewares.auth import authunticated , is_admin
from app.controllers.auth import signup as signupRoute , login as loginRoute , logoutRoute
from app.controllers.user import getUsersRoute , getMe
from app.controllers.recipe import createRecipeRoute , getAllRecipiesRoute
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

app.config['CORS_SUPPORTS_CREDENTIALS'] = True
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/v1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

# importing Models and exporting them
Users = User.UsersModel(db)
RefreshTokens = RefreshToken.RefreshTokensModel(db)
Ingredients = Ingrediant.IngredientsModel(db)
# Tags = Tag.TagsModel(db)
Recipes = Recipe.RecipesModel(db , Ingredients )
Plannings = Planning.PlanningsModel(db)
PlanningRecipes = PlanningRecipe.PlanningRecipesModel(db)

# db.init_app(app)
is_authenthicated = authunticated(db , Users)

@app.route('/')
def index():
    return "welcome to recipes-app api"


#*#################
#*   AUTH ROUTES  #
#*#################
@app.post('/signup')
def signup():
   return signupRoute(db , Users)

@app.post('/login')
def login():
   return loginRoute(db , Users)

@app.delete('/logout')
def logout() :
    return logoutRoute()

#*##################
#*  RECIPES ROUTES #
#*##################
@app.post('/recipes')
@is_authenthicated
def createRecipe(user):
    return createRecipeRoute(db , Recipes , Ingredients , user)

@app.get('/recipes')
def getAllrecipes():
    return getAllRecipiesRoute(db , Recipes)


#*#################
#*   USER ROUTES  #
#*#################
@app.get('/users')
@is_authenthicated
@is_admin
def getUsers(user):
  return getUsersRoute(db,  Users)

@app.get('/me')
@is_authenthicated
def getProfile(user):
    return getMe(user)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True ,  port=8081 , host="0.0.0.0" , use_reloader=True)
    