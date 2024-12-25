from extensions import db
from .base_model import BaseModel

class SingleItems(BaseModel):
    __tablename__ = 'single_items'
    name = db.Column(db.String(255), nullable=False)
    menu_id = db.Column(db.String(36), db.ForeignKey('menus.id'), nullable=False)
    grocer_id = db.Column(db.String(36), db.ForeignKey('grocers.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)