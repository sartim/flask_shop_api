from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.constants import Message
from app.helpers import validator
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
        body = request.data
        keys = ['name']
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
            name = body['name']
            status = OrderStatus(name=name)
            try:
                status.create(status)
                status.save()
                app.logger.debug(Message.SUCCESS)
                return jsonify(message=Message.SUCCESS), 201
            except Exception as e:
                app.exception("{}. {}".format(Message.ERROR, str(e)))
                return jsonify(message="Could not save record!"), 400
        else:
            app.logger.warning('Content type header is not application/json')
            return jsonify(message='Content-type header is not application/json'), 400

    @cross_origin()
    @jwt_required
    def put(self):
        body = request.data
        keys = ['id', 'name']
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
            status = OrderStatus.get_by_id(id)
            try:
                status.name = body['name']
                status.save()
                app.logger.debug(Message.SUCCESS)
                return jsonify(message=Message.SUCCESS), 200
            except Exception as e:
                app.exception("{}. {}".format(Message.ERROR, str(e)))
                return jsonify(message="Could not save record!"), 400
        else:
            app.logger.warning('Content type header is not application/json')
            return jsonify(message='Content-type header is not application/json'), 400

    @cross_origin()
    @jwt_required
    def delete(self):
        pass


app.add_url_rule('/order/status/', view_func=OrderStatusApi.as_view('order-statuses'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
