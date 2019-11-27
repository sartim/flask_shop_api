from app import db
from app.core.models import BaseModel


class Status(BaseModel):
    __tablename__ = 'status'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)

    @classmethod
    def response(cls, status):
        return dict(
            id=status.id, name=status.name,
            created_at=status.created_at,
            updated_at=status.updated_at
        )
