from extensions import db
from .base_model import BaseModel

class Orders(BaseModel):
    __tablename__ = 'orders'
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    grocer_id = db.Column(db.String(36), db.ForeignKey('grocers.id'), nullable=False)
    basket_id = db.Column(db.String(36), db.ForeignKey('baskets.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_id = db.Column(db.String(36), db.ForeignKey('transactions.id'))
    items = db.Column(db.JSON, default=[])