from extensions import db
from .base_model import BaseModel

class Transactions(BaseModel):
    __tablename__ = 'transactions'
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    grocer_id = db.Column(db.String(36), db.ForeignKey('grocers.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('NOT_YET_ORDERED', 'ORDERED', 'PENDING', 'PROCESSING', 'SUCCESS'), default='NOT_YET_ORDERED')