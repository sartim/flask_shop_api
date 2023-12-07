from app.core.app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    product_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product.id'))
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, product_id, rating, review=None, deleted=None):
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.deleted = deleted

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.product_id, self.user_id)
