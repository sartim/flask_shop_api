from flask import jsonify
from app import jwt
from app.user.models import User


@jwt.user_identity_loader
def user_loader_callback(identity):
    if not User.get_user_by_email(identity):
        return None
    return User.get_user_by_email(identity).email


@jwt.user_lookup_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404


@jwt.expired_token_loader
def expired_token_callback(header, data):
    token_type = data['type']
    return jsonify({
        'message': 'The {} token has expired'.format(token_type)
    }), 401
