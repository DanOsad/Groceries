from extensions import db
from .base_model import BaseModel

class Baskets(BaseModel):
    __tablename__ = 'baskets'
    id = db.Column(db.String(36), primary_key=True)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)