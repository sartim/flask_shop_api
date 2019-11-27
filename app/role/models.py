from app import db
from app.core.models import BaseModel


class Role(BaseModel):
    __tablename__ = 'role'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.name)


class RolePermission(BaseModel):
    __tablename__ = 'role_permission'

    role_id = db.Column(db.ForeignKey('role.id'))
    permission_id = db.Column(db.ForeignKey('permission.id'))

    db.relationship('Role', lazy=True)
    db.relationship('Permission', lazy=True)

    def __init__(self, role_id=None, permission_id=None):
        self.role_id = role_id
        self.permission_id = permission_id

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)
