from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from order.status.models import OrderStatus


class OrderStatusApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        id = request.args.get('id')
        if id:
            status = OrderStatus.get_by_id(id)
            result = status.__dict__
            del result['_sa_instance_state']
            return jsonify(result), 200
        statuses = OrderStatus.get_all(page)
        return jsonify(statuses), 200

    @cross_origin()
    @jwt_required
    def post(self):
        pass

    @cross_origin()
    @jwt_required
    def put(self):
        pass

    @cross_origin()
    @jwt_required
    def delete(self):
        pass


app.add_url_rule('/order/status/', view_func=OrderStatusApi.as_view('order-statuses'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
