from flask import jsonify, request
from app import app, jwt


@app.before_request
def handle_method_not_allowed():
    if request.routing_exception:
        if request.routing_exception.code == 405:
            return jsonify(message=request.routing_exception.description), 405


@app.errorhandler(404)
def resource_not_found(e):
    message = str(e).split(":")
    return jsonify(message=message[1].strip()), 404


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'message': 'The {} token has expired'.format(token_type)
    }), 401
