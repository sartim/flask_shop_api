from app import db
from app.core.models import BaseModel


class Role(BaseModel):
    __tablename__ = 'role'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, self.name)

    @classmethod
    def build_paginated_response(cls, roles, url):
        results = []
        for role in roles.items:
            data = cls.get_dict(id=role.id, name=role.name, created_at=role.created_at.isoformat(),
                                updated_at=role.updated_at.isoformat())
            results.append(data)
        data = cls.build_response(roles, results, url)
        return data
