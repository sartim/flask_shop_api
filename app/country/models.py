from app import db
from app.core.models import Base


class Country(Base):
    name = db.Column(db.String(255))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)
