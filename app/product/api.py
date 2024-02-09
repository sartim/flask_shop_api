import csv

from datetime import datetime
from io import StringIO
from flask import make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

from app.core.base_resource import BaseResource, UnauthorizedBaseResource
from app.product.models import Product
from app.product.schemas import ProductSchema, product_args_schema


class ProductApi(UnauthorizedBaseResource):
    model = Product
    schema = ProductSchema
    request_args = product_args_schema


class DownloadProductApi(BaseResource):
    decorators = [cross_origin(), jwt_required()]

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
