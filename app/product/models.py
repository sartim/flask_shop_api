import os

from sqlalchemy import desc
from sqlalchemy_utils import aggregated
from app.core.mixins import SearchableMixin
from app.core.base_model import BaseModel
from app import db
from app.category.models import Category
from app.review.models import Review


class Product(BaseModel, SearchableMixin):

    __tablename__ = 'products'
    __searchable__ = ['name', 'brand', 'category']

    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    items = db.Column(db.Integer)
    image_urls = db.Column(db.Text, nullable=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))

    category = db.relationship(Category, lazy=True)
    reviews = db.relationship(Review, lazy=True)

    def __init__(self, name=None, brand=None, items=None, image_urls=None, price=None, category_id=None):
        self.name = name
        self.brand = brand
        self.items = items
        self.image_urls = image_urls
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @aggregated('reviews', db.Column(db.Numeric))
    def avg_rating(self):
        return db.func.avg(Review.rating)

    @classmethod
    def get_by_id(cls, id):
        product = cls.query.filter_by(id=id).first()
        return cls.response(product)

    @classmethod
    def get_by_category(cls, category_id, page):
        products = cls.query.filter_by(category_id=category_id).\
            paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=True)
        results = []
        for product in products.items:
            data = cls.response(product)
            results.append(data)
        data = cls.response_dict(products, results, 'product/', category_id=category_id)
        return data

    @classmethod
    def get_all(cls, page):
        products = cls.query.order_by(desc(cls.created_date)).\
            paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=True)
        results = []
        for product in products.items:
            data = cls.response(product)
            results.append(data)
        data = cls.response_dict(products, results, 'product/')
        return data

    @classmethod
    def response(cls, product):
        return dict(id=product.id, name=product.name, brand=product.brand, items=product.items,
                    price=float(product.price) if product.price else None,
                    category=product.category.name if product.category else None,
                    created_date = product.created_date)
