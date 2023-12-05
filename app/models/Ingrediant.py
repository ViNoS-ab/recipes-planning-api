from dataclasses import dataclass

def IngredientsModel (db):
    @dataclass
    class Ingredients(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String, nullable=False)
        recipes = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    return IngredientsModel
