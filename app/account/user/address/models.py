from app import db


class AccountAddress(db.Model):

    __tablename__ = 'account_user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    country = db.Column(db.String(255))
    city_or_state = db.Column(db.String(255))
    address = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, user_id=None, country=None, city_or_state=None, address=None):
        self.user_id = user_id
        self.country = country
        self.city_or_state = city_or_state
        self.address = address

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)
