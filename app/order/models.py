from app.core.models import Base
from app import db


class Order(Base):
    __tablename__ = 'orders'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    def __init__(self, user_id=None, product_id=None, status_id=None, quantity=None):
        self.user_id = user_id
        self.product_id = product_id
        self.status_id = status_id
        self.quantity = quantity

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def get_orders_by_filter(cls, filter_):
        pass