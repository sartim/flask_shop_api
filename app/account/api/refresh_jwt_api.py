from flask import jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity
from app import app


class RefreshJwt(MethodView):
    @cross_origin()
    @jwt_refresh_token_required
    def post(self):
        """
        The jwt_refresh_token_required decorator insures a valid refresh
        token is present in the request before calling this endpoint. We
        can use the get_jwt_identity() function to get the identity of
        the refresh token, and use the create_access_token() function again
        to make a new access token for this identity.
        :return:
        """
        current_user = get_jwt_identity()
        ret = dict(access_token=create_access_token(identity=current_user))
        return jsonify(ret), 200


app.add_url_rule('/account/user/refresh/jwt/', view_func=RefreshJwt.as_view('account-refresh-token'), methods=['POST'])
