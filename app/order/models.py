import os
import flask

from datetime import date, timedelta, datetime
from sqlalchemy import func, extract, desc

from app.core.models import BaseModel
from app import db
from app.core import constants
from app.status.models import Status


class Order(BaseModel):
    __tablename__ = 'order'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    order_total = db.Column(db.DECIMAL(precision=10, scale=2),
                            nullable=True)

    user = db.relationship('User', lazy=True)
    status = db.relationship(Status, lazy=True)
    items = db.relationship('OrderItem',
                            cascade="save-update, merge, delete",
                            lazy=True)

    def __init__(self, user_id=None, status_id=None, order_total=None):
        self.user_id = user_id
        self.status_id = status_id
        self.order_total = order_total

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def response(cls, order):
        return dict(
            id=order.id,
            customer=order.customer.get_full_name if order.customer else None,
            user=order.user.get_full_name,
            status=order.status.name,
            items=[
                dict(
                    product=item.product.name, price=float(item.price),
                    quantity=item.quantity
                ) for item in order.items],
            total=float(
                order.order_total) if order.order_total else None,
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat()
        )

    @classmethod
    def get_by_id_data(cls, order_id):
        order = cls.get_by_id(order_id)
        data = cls.response(order)
        return data

    @classmethod
    def build_paginated_response(cls, orders, url):
        results = []
        for order in orders.items:
            data = cls.response(order)
            results.append(data)
        data = cls.build_response(orders, results, url)
        return data

    @classmethod
    def get_order_count(cls, status_id):
        return dict(
            count=cls.query.filter_by(status_id=status_id).count())

    @classmethod
    def get_all_by_status_body(cls, status_id, page):
        orders = cls.query.filter_by(status_id=status_id).order_by(
            desc(cls.created_at)) \
            .paginate(
            page=page,
            per_page=int(os.environ.get('PAGINATE_BY')),
            error_out=True
        )
        return cls.build_paginated_response(orders,
                                            flask.request.full_path)

    @classmethod
    def get_order_items(cls, order_id):
        order = cls.get_by_id(order_id)
        results = []
        for order_item in order.items:
            data = cls.get_dict(
                id=order_item.order.id, order_id=order_item.order_id,
                price=float(order_item.price),
                quantity=order_item.quantity,
                created_at=order_item.created_at.isoformat(),
                updated_at=order_item.updated_at.isoformat()
            )
            results.append(data)
        return {"count": len(results), "results": results}

    @classmethod
    def get_today_sum(cls):
        orders_today = cls.filter_all_today()
        total_sum = orders_today.with_entities(
            func.sum(cls.order_total).label("total_sum")).scalar()
        return dict(total_sum=int(total_sum))

    @classmethod
    def get_today(cls):
        orders_today = cls.filter_all_today()
        count = orders_today.filter(
            cls.created_at == func.date(cls.created_at) == date.today()) \
            .filter_by(status_id=5).count()
        return dict(count=count)

    @classmethod
    def get_this_month(cls):
        orders_this_month = cls.filter_all_this_month()
        count = orders_this_month.filter_by(status_id=5).count()
        return dict(count=count)

    @classmethod
    def get_last_month(cls):
        order_last_month = cls.filter_all_last_month()
        count = order_last_month.filter_by(status_id=5).count()
        return dict(count=count)

    @classmethod
    def get_this_year(cls):
        orders_this_year = cls.filter_all_this_year()
        count = orders_this_year.filter_by(status_id=5).count()
        return dict(count=count)

    @classmethod
    def get_last_year(cls):
        orders_this_year = cls.filter_all_this_year()
        count = orders_this_year.filter_by(status_id=5).count()
        return dict(count=count)

    @classmethod
    def get_daily_count(cls):
        query = cls.query \
            .with_entities(func.count(cls.id).label("count"),
                           func.date(cls.created_at).label(
                               "created_at"), ) \
            .filter_by(status_id=5)
        results = query.group_by(func.date(cls.created_at)) \
            .order_by(desc(func.date(cls.created_at))) \
            .all()
        orders = [dict(count=v.count, date=v.created_at.isoformat()) for
                  v in results]
        return orders

    @classmethod
    def get_orders_by_filter(cls, period):
        if period == 'daily':
            return cls.get_daily_count()
        if period == 'today':
            return cls.get_today()
        if period == 'yesterday':
            return cls.get_yesterday()
        if period == 'this-month':
            return cls.get_this_month()
        if period == 'last-month':
            return cls.get_last_month()
        if period == 'this-year':
            return cls.get_this_year()
        if period == 'last_year':
            return cls.get_last_year()


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),
                         primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    quantity = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    order = db.relationship('Order', lazy=True)
    product = db.relationship('Product', lazy=True)

    def __init__(self, order_id, product_id, price, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return "%s(%s, %s)" % (
            self.__class__.__name__, self.order_id, self.product_id)

    @classmethod
    def get_all_by_order_id_body(cls, order_id, page):
        order_items = cls.query.filter_by(order_id=order_id).order_by(
            desc(cls.created_at)) \
            .paginate(
            page=page,
            per_page=int(os.environ.get('PAGINATE_BY')),
            error_out=True
        )
        results = []
        for order_item in order_items.items:
            data = cls.get_dict(
                id=order_item.id,
                order_id=order_item.order_id,
                price=order_item.price,
                quantity=order_item.quantity,
                created_at=order_item.created_at.isoformat(),
                updated_at=order_item.updated_at.isoformat()
            )
            results.append(data)
        return BaseModel.build_response(
            order_items, results,
            flask.request.url
        )

    def create(self):
        db.session.add(self)
        BaseModel.save()
