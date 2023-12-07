from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from app.core.mixins import SearchableMixin
from app.core.base_model import BaseModel
from app.core.app import db
from app.category.models import Category
from app.review.models import Review


class Product(BaseModel, SearchableMixin):

    __tablename__ = 'product'
    __searchable__ = ['name', 'brand', 'category']

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    items = db.Column(db.Integer)
    image_urls = db.Column(db.Text, nullable=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))

    category = db.relationship(Category, lazy=True)
    reviews = db.relationship(Review, lazy=True)

    def __init__(self, id=None, name=None, brand=None, items=None, image_urls=None, price=None, category_id=None):
        self.id = id
        self.name = name
        self.brand = brand
        self.items = items
        self.image_urls = image_urls
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)
