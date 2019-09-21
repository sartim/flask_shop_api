from app import db
from app.core.models import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'

    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    products = db.relationship('Product', lazy=True)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<%r (%r)" % (self.__class__.__name__, self.id)

    @classmethod
    def response(cls, category):
        return dict(
            id=category.id, name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )

    @classmethod
    def build_paginated_response(cls, categories, url):
        results = []
        for category in categories.items:
            data = cls.response(category)
            results.append(data)
        data = cls.build_response(categories, results, url)
        return data
