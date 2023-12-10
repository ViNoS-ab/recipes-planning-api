from dataclasses import dataclass 

def RecipesModel (db , Ingredients ):
    @dataclass
    class Recipes(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String, nullable=False)
        description = db.Column(db.String)
        added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        ingrediants = db.relationship("Ingredients" , backref="recipes" , secondary="recipe_ingrediant")
        time = db.Column(db.String)
        image = db.Column(db.String)
        
    db.Table("recipe_ingrediant" ,
             db.Column("recipe_id" , db.Integer , db.ForeignKey("recipes.id")),
             db.Column("ingrediant_id" , db.Integer , db.ForeignKey("ingredients.id"))
             )
    return Recipes