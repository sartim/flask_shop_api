from app import db
from app.core.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    name = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.id)
