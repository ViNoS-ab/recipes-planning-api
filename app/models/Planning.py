from dataclasses import dataclass 

def PlanningsModel (db):
    @dataclass
    class Plannings(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        private = db.Column(db.Boolean, default=True)
    return Plannings