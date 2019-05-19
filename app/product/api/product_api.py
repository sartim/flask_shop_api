from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.product.models import Product


class ProductApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        id = request.args.get('id')
        if id:
            product = Product.get_by_id(id)
            return jsonify(product), 200
        products = Product.get_all(page)
        return jsonify(products), 200

    @cross_origin()
    @jwt_required
    def post(self):
        return jsonify(), 201

    @cross_origin()
    @jwt_required
    def put(self):
        return jsonify(), 200

    @cross_origin()
    @jwt_required
    def delete(self):
        return jsonify(), 200


app.add_url_rule('/product/', view_func=ProductApi.as_view('products'), methods=['GET', 'POST', 'PUT','DELETE'])
