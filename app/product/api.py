import csv

from io import StringIO
from datetime import datetime
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

from app import app
from app.core.api import BaseResource
from app.core.helpers.decorators import content_type, validate
from app.product.models import Product, ProductCategory


class ProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, product_id=None):
        page = request.args.get('page')
        if product_id is None:
            products = Product.get_all_data(int(page) if page else None)
            return self.response(products)
        product = Product.get_by_id_data(product_id)
        return self.response(product)

    @content_type(['application/json'])
    @validate(['name', 'description'])
    def post(self):
        product = Product(**request.json)
        save, message, obj = product.create()
        if save:
            app.logger.debug(message)
            result = dict(product_id=obj.id)
            return self.response(result, 201)
        result = dict(message=message)
        return self.response(result, 400)

    @content_type(['application/json'])
    def put(self, product_id=None):
        product = Product.get_by_id(id=product_id)
        if not product:
            result = dict(message="Id not found!")
            return self.response(result, 404)
        updated = Product.update(product_id, **request.json)
        if not updated:
            result = dict(message="Did not update!")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, status=201)

    def delete(self, product_id=None):
        product = Product.get_by_id(product_id)
        if not product:
            result = dict(message="Id not found!")
            return self.response(result, status=404)
        result = product.delete()
        product.save()
        if result:
            result = dict(message="Successfully deleted {}!".format(product_id))
            return self.response(result)
        result = dict(message="{} Not deleted!".format(product_id))
        return self.response(result, 400)


class DownloadProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['id', 'name', 'description', 'cost_price', 'selling_price', 'stock', 'size'])
        users = Product.query.order_by(desc(Product.created_at)).all()
        for obj in users:
            cw.writerow([obj.id, obj.name, obj.description, obj.cost_price, obj.stock, obj.size])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename={}_{}.csv".format("all_products", datetime.now())
        output.headers["Content-type"] = "text/csv"
        si.close()
        return output


class ProductCategoryApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, category_id=None):
        page = request.args.get('page')
        if category_id is None:
            product_categories = ProductCategory.get_all_data(int(page) if page else None)
            return self.response(product_categories)
        product_category = Product.get_by_id_data(category_id)
        return self.response(product_category)

    @content_type(['application/json'])
    @validate(['name', 'description'])
    def post(self):
        product_category = ProductCategory(**request.json)
        save, message, obj = product_category.create()
        if save:
            app.logger.debug(message)
            result = dict(product_category=obj.id)
            return self.response(result, 201)
        result = dict(message=message)
        return self.response(result, 400)

    @content_type(['application/json'])
    def put(self, category_id=None):
        product_category = Product.get_by_id(id=category_id)
        if not product_category:
            result = dict(message="Id not found!")
            return self.response(result, 404)
        updated = ProductCategory.update(category_id, **request.json)
        if not updated:
            result = dict(message="Did not update!")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, status=201)

    def delete(self, category_id=None):
        product_category = ProductCategory.get_by_id(category_id)
        if not product_category:
            result = dict(message="Id not found!")
            return self.response(result, status=404)
        result = product_category.delete()
        product_category.save()
        if result:
            result = dict(message="Successfully deleted {}!".format(category_id))
            return self.response(result)
        result = dict(message="{} Not deleted!".format(category_id))
        return self.response(result, 400)

class DownloadProductCategoryApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['id', 'name', 'description', 'created_at', 'updated_at'])
        product_categories = ProductCategory.query.order_by(desc(ProductCategory.created_at)).all()
        for obj in product_categories:
            cw.writerow([obj.id, obj.name, obj.description, obj.created_at.isoformat(), obj.updated_at.isoformat()])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename={}_{}.csv".format("all_product_categories",
                                                                                        datetime.now())
        output.headers["Content-type"] = "text/csv"
        si.close()
        return output
