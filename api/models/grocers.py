from extensions import db
from .base_model import BaseModel

class Grocers(BaseModel):
    __tablename__ = 'grocers'
    name = db.Column(db.String(255), nullable=False)