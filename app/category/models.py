from app import db
from app.core.models import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    products = db.relationship('Product', lazy=True)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)
