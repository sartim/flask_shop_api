from app import db
from app.core.base_model import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permission'

    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, name=None, description=None, deleted=None):
        self.name = name
        self.description = description
        self.deleted = deleted

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.name)
