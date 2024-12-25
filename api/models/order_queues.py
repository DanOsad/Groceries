from extensions import db
from .base_model import BaseModel

class OrderQueues(BaseModel):
    __tablename__ = 'order_queues'
    grocer_id = db.Column(db.String(36), db.ForeignKey('grocers.id'), nullable=False)
    baskets = db.Column(db.JSON, default=[])