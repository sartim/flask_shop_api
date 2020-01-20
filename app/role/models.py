from app import db
from app.core.base_model import BaseModel, AbstractBaseModel


class Role(BaseModel):
    __tablename__ = 'role'

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    permissions = db.relationship("RolePermission", lazy=True)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)




class RolePermission(AbstractBaseModel):
    __tablename__ = 'role_permission'

    role_id = db.Column(db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(
        db.ForeignKey('permission.id'), primary_key=True
    )

    role = db.relationship('Role', lazy=True)
    permission = db.relationship('Permission', lazy=True)

    def __init__(self, role_id=None, permission_id=None):
        self.role_id = role_id
        self.permission_id = permission_id

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)

    @classmethod
    def get_role_permission_data(cls, schema, role_id):
        role_permission = cls.query.filter_by(role_id=role_id).all()
        res = [cls.to_dict(schema, v) for v in role_permission]
        return res
