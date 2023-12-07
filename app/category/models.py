from app.core.app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from app.core.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, id=None, name=None, description=None, deleted=None):
        self.id = id
        self.name = name
        self.description = description
        self.deleted = deleted

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.id)
