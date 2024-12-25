from extensions import db

class BaseModel(db.Model):
    __abstract__ = True  # This makes sure SQLAlchemy knows not to create a table for this class
    id = db.Column(db.String(36), primary_key=True)

    @property
    def as_dict(self):
        return { column.name: getattr(self, column.name) for column in self.__table__.columns }

    @property
    def serialize(self):
        return { attr: getattr(self, attr) for attr in self.columns }
    
    @property
    def columns(self):
        return [ column.name for column in self.__table__.columns ]
