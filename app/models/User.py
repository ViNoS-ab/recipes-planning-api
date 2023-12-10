from dataclasses import dataclass , fields
from sqlalchemy import Enum


def UsersModel(db) :
    @dataclass
    class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True, unique=True)
        username = db.Column(db.String(255), nullable=False)
        role = db.Column(Enum("user" , "admin"), default="user")
        created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
        updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
        password = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False , unique=True)
        verified = db.Column(db.Boolean, default=False)
    return Users