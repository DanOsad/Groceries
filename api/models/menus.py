from extensions import db
from .base_model import BaseModel

class Menus(BaseModel):
    __tablename__ = 'menus'
    grocer_id = db.Column(db.String(36), db.ForeignKey('grocers.id'), nullable=False)