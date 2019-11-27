from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)

from app import app
from app.core.api import BaseResource
from app.core.helpers import utils
from app.core.helpers.decorators import validate, content_type
from app.user.models import User


class GenerateJwtApi(BaseResource):
    decorators = [cross_origin()]

    @content_type(['application/json'])
    @validate(['email', 'password'])
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        if not request.is_json:
            result = dict(message="Missing JSON in request")
            return self.response(result, 400)
        user = User.get_user_by_email(email)
        if user:
            if utils.check_password_hash(user.password, password):
                app.logger.info(
                    "Logged in user with the email {0}".format(email))
                access_token = create_access_token(
                    identity=email,
                    expires_delta=False
                )
                refresh_token = create_refresh_token(identity=email)
                result = dict(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    user=dict(
                        id=user.id,
                        full_name="{} {}".format(
                            user.first_name,
                            user.last_name),
                        email=user.email,
                        roles=[user_role.role.name for user_role in user.roles]
                    )
                )
                return self.response(result)
        else:
            app.logger.warning(
                "User with the email {0} does not exist".format(email))
            result = dict(message="Bad username or password")
            return self.response(result, 401)


class RefreshJwtApi(BaseResource):
    decorators = [cross_origin(), jwt_refresh_token_required]

    def post(self):
        current_user = get_jwt_identity()
        result = dict(
            access_token=create_access_token(identity=current_user))
        return self.response(result)
