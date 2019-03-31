from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.order.models import Order


class OrderApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        filter_ = request.args.get('filter_')
        if filter_:
            orders = Order.get_orders_by_filter(filter_)
            return jsonify(count=orders)
        return jsonify(message='Missing path variable'), 400

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


app.add_url_rule('/order/', view_func=OrderApi.as_view('orders'), methods=['GET', 'POST', 'PUT','DELETE'])
