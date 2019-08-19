import os

from flask import request

from app import db
from app.core.models import BaseModel

class Product(BaseModel):
    __tablename__ = 'products'

    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    cost_price = db.Column(db.DECIMAL(precision=10, scale=2))
    selling_price = db.Column(db.DECIMAL(precision=10, scale=2))
    stock = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    images = db.Column(db.Text, nullable=True)

    category = db.relationship('ProductCategory', lazy=True)
    supplier = db.relationship('Supplier', lazy=True)

    def __init__(self, name=None, description=None, cost_price=None, selling_price=None, stock=None, size=None,
                 category_id=None, supplier_id=None, images=None):
        self.name = name
        self.description = description
        self.cost_price = cost_price
        self.selling_price = selling_price
        self.stock = stock
        self.size = size
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.images = images

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.id)

    @classmethod
    def get_by_id_body(cls, id):
        product = cls.get_by_id(id)
        data = product.get_dict(id=product.id, name=product.name, description=product.description,
                                cost_price=float(product.cost_price), selling_price=float(product.selling_price),
                                category=product.category.name, stock=product.stock, size=product.size,
                                images=["{}uploads/{}".format(request.url_root, v.lstrip()) for v in
                                        product.images.split(',')],
                                created_at=product.created_at.isoformat(),
                                updated_at=product.updated_at.isoformat())
        return data

    @classmethod
    def get_by_ids_body(cls, ids, page):
        product = cls.query.filter(cls.id.in_(ids)).paginate(page=page,
                                                             per_page=int(os.environ.get('PAGINATE_BY')),
                                                             error_out=True)
        return cls.build_paginated_response(product, request.full_path)

    @classmethod
    def build_paginated_response(cls, products, url):
        results = []
        for product in products.items:
            data = cls.get_dict(id=product.id, name=product.name, description=product.description,
                                cost_price=float(product.cost_price), selling_price=float(product.selling_price),
                                category=product.category.name, stock=product.stock, size=product.size,
                                images=["{}uploads/{}".format(request.url_root, v.lstrip()) for v in
                                        product.images.split(',')],
                                created_at=product.created_at.isoformat(),
                                updated_at=product.updated_at.isoformat())
            results.append(data)
        data = cls.build_response(products, results, url)
        return data


class ProductCategory(BaseModel):
    __tablename__ = 'product_categories'

    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    products = db.relationship('Product', lazy=True)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.id)

    @classmethod
    def get_by_id_body(cls, id):
        product = cls.get_by_id(id)
        data = product.get_dict(id=product.id, name=product.name, description=product.description,
                                created_at=product.created_at.isoformat(),
                                updated_at=product.updated_at.isoformat())
        return data

    @classmethod
    def build_paginated_response(cls, product_categories, url):
        results = []
        for product_category in product_categories.items:
            data = cls.get_dict(id=product_category.id, name=product_category.name,
                                description=product_category.description,
                                created_at=product_category.created_at.isoformat(),
                                updated_at=product_category.updated_at.isoformat())
            results.append(data)
        data = cls.build_response(product_categories, results, url)
        return data


class Review(db.Model):
    __tablename__ = 'ratings'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=True)

    def __init__(self, product_id, rating, review=None):
        self.product_id = product_id
        self.rating = rating
        self.review = review

    def __repr__(self):
        return "<%s(%s, %s)>" % (self.__class__.__name__, self.product_id, self.user_id)
