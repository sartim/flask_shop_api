from flask import jsonify
from app import jwt
from app.user.models import User


@jwt.user_identity_loader
def user_loader_callback(identity):

    if not User.get_user_by_email(identity):
        return None

    return User.get_user_by_email(identity)


@jwt.user_lookup_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404
