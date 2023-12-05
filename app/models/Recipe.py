from dataclasses import dataclass 

def RecipesModel (db):
    @dataclass
    class Recipes(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String, nullable=False)
        description = db.Column(db.String)
        added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    return Recipes