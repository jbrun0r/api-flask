from .. import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    age = db.Column(db.String(3), nullable=False)
