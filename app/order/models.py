from app.core.base_model import BaseModel
from app import db
from app.status.models import Status
from sqlalchemy.dialects.postgresql import UUID


class Order(BaseModel):
    __tablename__ = 'order'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    status_id = db.Column(UUID(as_uuid=True), db.ForeignKey('status.id'))
    order_total = db.Column(
        db.DECIMAL(precision=10, scale=2),
        nullable=True
    )

    user = db.relationship('User', lazy=True)
    status = db.relationship(Status, lazy=True)
    items = db.relationship('OrderItem',
                            cascade="save-update, merge, delete",
                            lazy=True)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, id=None, user_id=None, status_id=None, deleted=None):
        self.id = id
        self.user_id = user_id
        self.status_id = status_id
        self.deleted = deleted

    def __repr__(self):
        return "<%r (%r)" % (self.__class__.__name__, self.id)


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id = db.Column(
        db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product.id'), primary_key=True)
    price = db.Column(db.DECIMAL(precision=10, scale=2))
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    order = db.relationship('Order', lazy=True, overlaps="items")
    product = db.relationship('Product', lazy=True)

    def __init__(self, order_id, product_id, price, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return "%s(%s, %s)" % (
            self.__class__.__name__, self.order_id, self.product_id)
