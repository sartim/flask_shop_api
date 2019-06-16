from app import db


class Review(db.Model):
    __tablename__ = 'ratings'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text, nullable=True)

    def __init__(self, product_id, rating, review=None):
        self.product_id = product_id
        self.rating = rating
        self.review = review

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.product_id, self.user_id)
