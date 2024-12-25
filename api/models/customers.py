import uuid
from extensions import db
from .base_model import BaseModel

class Customers(BaseModel):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = db.Column(db.String(255), nullable=False)
