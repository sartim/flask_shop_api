from flask import jsonify
from flask.views import MethodView


class BaseResource(MethodView):
    @staticmethod
    def response(data, status=200):
        return jsonify(data), status
