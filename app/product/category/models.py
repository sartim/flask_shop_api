import os

from app.core.models import Base
from app import db


class ProductCategory(Base):
    __tablename__ = 'product_categories'

    name = db.Column(db.String(255))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def response(cls, categories):
        results = []
        for category in categories.items:
            data = dict(id=category.id, product=category.name,created_date=category.created_date)
            results.append(data)
        data = cls.response_dict(categories, results, '/product/category/')
        return data

    @classmethod
    def get_all(cls, page):
        categories = cls.query.paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=True)
        data = cls.response(categories)
        return data
