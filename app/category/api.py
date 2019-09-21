from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.api import BaseResource
from app.product.models import Product
from app.category.models import Category


class CategoryApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, category_id=None):
        page = request.args.get('page')
        if category_id:
            category = Category.get_by_id_data(category_id)
            return self.response(category)
        category = Category.get_all_data(int(page) if page else None)
        return self.response(category)

    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        category = Category(**request.json)
        category.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, category_id=None):
        category = Product.get_by_id(category_id)
        if not category:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Product.update(id, **request.json)
        if not updated:
            result = dict(message="Did not update product.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, category_id=None):
        category = Category.get_by_id(category_id)
        if not category:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = category.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(id))
            return self.response(result, 204)
        result = dict(message="{} Not deleted".format(id))
        return self.response(result, 400)
