from app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from app.core.base_model import BaseModel, AbstractBaseModel


class Role(BaseModel):
    __tablename__ = 'role'

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    deleted = db.Column(db.Boolean, default=False)

    permissions = db.relationship("RolePermission", lazy=False)

    def __init__(self, id=None, name=None, description=None, deleted=None):
        self.id = id
        self.name = name
        self.description = description
        self.deleted = deleted

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)


class RolePermission(AbstractBaseModel):
    __tablename__ = 'role_permission'

    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('permission.id'), primary_key=True
    )

    role = db.relationship('Role', lazy=False, overlaps="permissions")
    permission = db.relationship('Permission', lazy=False)

    def __init__(self, role_id=None, permission_id=None):
        self.role_id = role_id
        self.permission_id = permission_id

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)
