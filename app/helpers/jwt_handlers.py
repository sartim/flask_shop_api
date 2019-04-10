from flask import jsonify
from app import jwt
from app.account.user.models import AccountUser


@jwt.user_loader_callback_loader
def user_loader_callback(identity):

    if not AccountUser.get_user_by_email(identity):
        return None

    return AccountUser.get_user_by_email(identity)

@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404
