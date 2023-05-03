from app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from app.core.base_model import BaseModel


class Status(BaseModel):
    __tablename__ = 'status'

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    name = db.Column(db.String(255), unique=True)

    def __init__(self, id=None, name=None):
        self.id = id
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
