from app import db
from app.core.models import BaseModel


class Status(BaseModel):
    __tablename__ = 'status'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)

    @classmethod
    def response(cls, expense):
        return dict(
            id=expense.id, user=expense.user.get_full_name, description=expense.description,
            amount=float(expense.amount), created_at=expense.created_at,
            updated_at=expense.updated_at
        )
