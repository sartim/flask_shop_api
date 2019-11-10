from app import db
from app.core.models import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permission'

    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)

    def __init__(self, name=None, description=description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)
