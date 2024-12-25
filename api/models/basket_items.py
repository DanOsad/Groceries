from extensions import db
from .base_model import BaseModel

class BasketItems(BaseModel):
    __tablename__ = 'basket_items'
    item_id = db.Column(db.String(36), nullable=False)  # foreign key to single_items or single_weighted_items
    basket_id = db.Column(db.String(36), db.ForeignKey('baskets.id'), nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Quantity or weight