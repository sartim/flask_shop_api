from app.core.models import Base
from app import db


class OrderStatus(Base):

    __tablename__ = 'order_statuses'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
