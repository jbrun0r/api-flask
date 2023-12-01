from sqlalchemy.dialects.postgresql import UUID
from .. import db
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    age = db.Column(db.String(3), nullable=False)
