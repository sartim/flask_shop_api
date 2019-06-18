from app import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    quantity = db.Column(db.Integer)

    def __init__(self, user_id, product_id, price, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.order_idm, self.product_id)

