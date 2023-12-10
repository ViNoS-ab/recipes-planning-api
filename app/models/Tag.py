from dataclasses import dataclass

def TagsModel (db):
    @dataclass
    class Tags(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String, nullable=True)

    return Tags
