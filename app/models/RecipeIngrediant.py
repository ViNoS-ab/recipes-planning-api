from dataclasses import dataclass

def RecipeIngredientsModel (db):
    @dataclass
    class RecipeIngredients(db.Model):
        Ingrediant = db.Column(db.Integer, db.ForeignKey('ingredients.id') ,nullable=False, primary_key=True )
        recipe = db.Column(db.Integer, db.ForeignKey('recipes.id') , nullable=False, primary_key=True )
        quantity= db.Column(db.Integer)
    return RecipeIngredientsModel
