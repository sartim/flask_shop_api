from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.order.models import Order
from app.core.constants import Message
from app.core.helpers import validator


class OrderApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        filter_ = request.args.get('filter_')
        page = request.args.get('page')
        if filter_:
            orders = Order.get_orders_by_filter(filter_, page)
            return jsonify(orders)
        orders = Order.get_all(page)
        return jsonify(orders), 400

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
            order = Order.get_by_id(id)
            try:
                order.delete()
                app.logger.debug(Message.SUCCESS)
                return jsonify(message=Message.SUCCESS), 200
            except Exception as e:
                app.exception("{}. {}".format(Message.ERROR, str(e)))
                return jsonify(message="Could not save record!"), 400
        else:
            app.logger.warning('Content type header is not application/json')
            return jsonify(message='Content-type header is not application/json'), 400


app.add_url_rule('/order/', view_func=OrderApi.as_view('orders'), methods=['GET', 'POST', 'PUT','DELETE'])
