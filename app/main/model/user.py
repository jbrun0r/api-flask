from .. import db

import enum


class Profile(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    OWNER = "OWNER"

    def __str__(self) -> str:
        return self.value

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    token = db.Column(db.String)
    activation_status = db.Column(db.Boolean, nullable=False, default=False)
    profile = db.Column(db.Enum(Profile), nullable=False)
