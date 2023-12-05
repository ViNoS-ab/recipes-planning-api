from dataclasses import dataclass 

def RefreshTokensModel (db):
    @dataclass
    class RefreshTokens(db.Model):
        userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
        token = db.Column(db.String, nullable=False, unique=True)
        created_at = db.Column(db.TIMESTAMP)
    return RefreshTokens
