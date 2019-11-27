import csv
import os

from datetime import datetime
from io import StringIO
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

from app.category.models import Category
from app.core.helpers import s3
from app.core.helpers.decorators import validate
from app.core.helpers.utils import allowed_file
from app.user.models import User
from app.core.api import BaseResource
from app.product.models import Product


class ProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, product_id=None):
        page = request.args.get('page')
        if product_id is None:
            products = Product.get_all_data(int(page) if page else None)
            return self.response(products)
        product = Product.get_by_id_data(product_id)
        return self.response(product)

    @validate([
        'name', 'description', 'cost_price', 'stock',
        'selling_price', 'size', 'category_id', 'supplier_id'
    ])
    def post(self):
        request_body = request.form.to_dict()
        file = request.files['image']
        image_url = s3.upload_file(file, os.environ.get("S3_BUCKET"))
        request_body['image'] = image_url
        product = Product(**request_body)
        product.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, product_id=None):
        description = request.json.get('description')
        amount = request.json.get('amount')
        product = Product.get_by_id(product_id)
        if not product:
            result = dict(message="Id not found")
            return self.response(result, 404)
        product.user_id = User.get_logged_in_id
        product.description = description if description \
            else product.description
        product.amount = amount if amount else product.amount
        product.save()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def delete(self, product_id=None):
        product = Product.get_by_id(product_id)
        if not product:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = product.delete()
        if result:
            result = dict(
                message="Successfully deleted {}".format(product_id)
            )
            return self.response(result, 204)
        result = dict(
            message="{} Not deleted".format(product_id)
        )
        return self.response(result, 400)


class DownloadProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['id', 'name', 'description', 'phone', 'email'])
        users = Product.query.order_by(desc(Product.created_at)).all()
        for obj in users:
            cw.writerow([
                obj.id, obj.name, obj.description,
                obj.phone, obj.email
            ])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; " \
                                                "filename={}_{}.csv" \
            .format("all_products", datetime.now())
        output.headers["Content-type"] = "text/csv"
        si.close()
        return output


class UploadProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    # @content_type(['multipart/form-data'])
    # @validate(['csv_file'])
    def post(self):
        file = request.files.get('csv_file')
        if file and allowed_file(file.filename, 'dataset'):
            items = [file.read().decode()]
            # csv_stream = csv.reader(items)
            for v in items:
                print(v)
            # for v in file.items:
            #     print(v)
        return self.response('')


class ProductCategoryApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, category_id=None):
        page = request.args.get('page')
        if category_id:
            product_category = Category.get_by_id_data(category_id)
            return self.response(product_category)
        product_categories = Category.get_all_data(
            int(page) if page else None
        )
        return self.response(product_categories)

    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        product_category = Category(**request.json)
        product_category.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, category_id=None):
        product_category = Product.get_by_id(category_id)
        if not product_category:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Product.update(id, **request.json)
        if not updated:
            result = dict(message="Did not update product.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, category_id=None):
        product_category = Category.get_by_id(category_id)
        if not product_category:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = product_category.delete()
        if result:
            result = dict(
                message="Successfully deleted {}".format(category_id)
            )
            return self.response(result, 204)
        result = dict(message="{} Not deleted".format(category_id))
        return self.response(result, 400)
