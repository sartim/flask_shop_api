import os

from datetime import date, timedelta, datetime
from sqlalchemy import func, extract
from app.core.mixins import SearchableMixin
from app.core.models import Base
from app import db, constants
from app.order.status.models import OrderStatus
from app.product.models import Product


class Order(Base, SearchableMixin):
    __tablename__ = 'orders'
    __searchable__ = ['id']

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'),
                        primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.id'),
                          primary_key=True)
    order_total = db.Column(db.DECIMAL(precision=10, scale=2))

    product = db.relationship(Product, backref='oder_product', lazy=True)
    status = db.relationship(OrderStatus, backref='oder_status', lazy=True)

    def __init__(self, user_id=None, product_id=None, status_id=None,
                 quantity=None):
        self.user_id = user_id
        self.product_id = product_id
        self.status_id = status_id
        self.quantity = quantity

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def response(cls, orders):
        results = []
        for order in orders.items:
            data = dict(id=order.id, product=order.product.name,
                        status=order.status.name,  quantity=order.quantity,
                        created_date=order.created_date)
            results.append(data)
        data = cls.response_dict(orders, results, '/account/user/')
        return data

    @classmethod
    def get_all(cls, page):
        orders = cls.query.paginate(page=page,
                                    per_page=int(os.environ.get('PAGINATE_BY')),
                                    error_out =True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_today(cls, page):
        orders = cls.query.filter(func.date(cls.created_date) == date.today())\
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_yesterday(cls, page):
        yesterday = date.today() - timedelta(days=1)
        orders = cls.query.filter(func.date(cls.created_date) == yesterday) \
            .filter(cls.status_id == constants.COMPLETE) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_this_month(cls, page):
        orders = cls.query\
            .filter(extract('year', cls.created_date) == datetime.now().year) \
            .filter(extract('month', cls.created_date) == datetime.now().month) \
            .filter(cls.status_id == constants.COMPLETE) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_last_month(cls, page):
        orders = cls.query\
            .filter(extract('year',
                            cls.created_date) == datetime.now().year) \
            .filter(extract('month',
                            cls.created_date) == datetime.now().month - 1) \
            .filter(cls.status_id == constants.COMPLETE) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_this_year(cls, page):
        orders = cls.query.filter(extract('year',
                                          cls.created_date) == datetime.now().year) \
            .filter(cls.status_id == constants.COMPLETE) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_last_year(cls, page):
        orders = cls.query.filter(extract('year',
                                          cls.created_date) == datetime.now().year - 1) \
            .filter(cls.status_id == constants.COMPLETE) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')),
                      error_out=True)
        data = cls.response(orders)
        return data

    @classmethod
    def get_orders_by_filter(cls, filter_, page):
        if filter_ == 'today':
            return cls.get_today(page)
        if filter_ == 'yesterday':
            return cls.get_yesterday(page)
        if filter_ == 'this-month':
            return cls.get_this_month(page)
        if filter_ == 'last-month':
            return cls.get_last_month(page)
        if filter_ == 'this-year':
            return cls.get_this_year(page)
        if filter_ == 'last_year':
            return cls.get_last_year(page)
