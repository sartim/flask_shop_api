from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, create_refresh_token
from app import app
from app.account.user.models import AccountUser
from app.core.helpers import utils


class GenerateJwt(MethodView):
    @cross_origin()
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return jsonify({"msg": "Missing email parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        user = AccountUser.get_user_by_email(email)
        if user:
            if utils.check_password_hash(user.password, password):
                app.logger.info("Logged in user with the email {0}".format(email))
                # Identity can be any data that is json serializable
                access_token = create_access_token(identity=email, expires_delta=False)
                refresh_token = create_refresh_token(identity=email)
                results = dict(
                    access_token=access_token, refresh_token=refresh_token,
                    user=dict(id=user.id, full_name="{} {}".format(user.first_name, user.last_name, email=user.email))
                )
                return jsonify(results), 200
            else:
                app.logger.warning("User with the email {0} does not exist".format(email), extra={'stack': True})
                return jsonify({"msg": "Bad username or password"}), 401
        else:
            app.logger.warning("User with the email {0} does not exist".format(email), extra={'stack': True})
            return jsonify({"msg": "Bad username or password"}), 401


app.add_url_rule('/account/generate/jwt/', view_func=GenerateJwt.as_view('account-generate-token'), methods=['POST'])
