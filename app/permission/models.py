from app.core.app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from app.core.base_model import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permission'

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    path = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(
            self, id=None, name=None, description=None,
            path=None, deleted=None):
        self.id = id
        self.name = name
        self.description = description
        self.path = path
        self.deleted = deleted

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.name)
