from dataclasses import dataclass 
from sqlalchemy import Enum

def PlanningRecipesModel (db):
    @dataclass
    class PlanningRecipes(db.Model):
        day = db.Column(Enum('SUNDAY', 'MONDAY', 'THURSDAY', 'WEDNESDAY', 'TUESDAY', 'FRIDAY', 'SATURDAY', name='days'), nullable=False)
        time = db.Column(db.String)
        recipe = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
        planning = db.Column(db.Integer, db.ForeignKey('plannings.id'), primary_key=True)
