from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.product.models import Product
from app.core.constants import Message
from app.core.helpers import validator


class ProductApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        id = request.args.get('id')
        category_id = request.args.get('category_id')
        if id:
            product = Product.get_by_id(id)
            return jsonify(product), 200
        if category_id:
            product = Product.get_by_category(category_id, int(page) if page else None)
            return jsonify(product), 200
        products = Product.get_all(int(page) if page else None)
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
        body = request.data
        keys = ['id']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning('{}: \n {}'.format(Message.VALIDATION_ERROR, body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('{}: \n {}'.format(Message.VALIDATION_ERROR, body))
                return jsonify(validated['data'])
            id = body['id']
            product = Product.get_by_id(id)
            try:
                product.delete()
                app.logger.debug(Message.SUCCESS)
                return jsonify(message=Message.SUCCESS), 200
            except Exception as e:
                app.exception("{}. {}".format(Message.ERROR, str(e)))
                return jsonify(message="Could not save record!"), 400
        else:
            app.logger.warning('Content type header is not application/json')
            return jsonify(message='Content-type header is not application/json'), 400


app.add_url_rule('/product/', view_func=ProductApi.as_view('products'), methods=['GET', 'POST', 'PUT','DELETE'])
