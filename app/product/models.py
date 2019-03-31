from app.core.models import Base
from app import db


class Product(Base):
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    items = db.Column(db.Integer)
    image_urls = db.Column(db.Text, nullable=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))


    def __init__(self, name=None, brand=None, items=None, image_urls=None, price=None, category_id=None):
        self.name = name
        self.brand = brand
        self.items = items
        self.image_urls = image_urls
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)
