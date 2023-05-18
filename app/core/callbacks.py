from flask import jsonify, request
from app import app, jwt


@app.route("/")
def root_api():
    return "Welcome", 200


@app.route("/server-status")
def server_status():
    return "", 200


@app.before_request
def handle_method_not_allowed():
    if request.routing_exception:
        if request.routing_exception.code == 405:
            return jsonify(message=request.routing_exception.description), 405


@app.errorhandler(404)
def resource_not_found(e):
    message = str(e).split(":")
    return jsonify(message=message[1].strip()), 404


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify(messages), err.code, headers
    else:
        return jsonify(messages), err.code
