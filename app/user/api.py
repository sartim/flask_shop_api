import csv

from datetime import datetime
from io import StringIO
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from app import app
from app.core.base_resource import BaseResource
from app.core.helpers.decorators import content_type, validator
from app.role.models import Role
from app.user.models import User, UserRole
from app.core.helpers import password_helper
from app.user.schemas import UserSchema


class UserApi(BaseResource):
    decorators = [cross_origin(), jwt_required]
    model = User
    schema = UserSchema()

    @content_type(["application/json"])
    @validator(schema)
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        body = request.json
        roles = request.json.get('roles')
        if "roles" in body:
            del body['roles']
        user_obj = User(**body).create()
        if roles:
            for role in roles:
                user_obj.roles.append(
                    UserRole(user_obj, Role.get_by_name(role).id))
                user_obj.save()
        if user_obj:
            result = dict(message="Successfully saved record!")
            return self.response(result, 201)
        else:
            result = dict(message="Could not save record!")
            return self.response(result, 400)

    @content_type(["application/json"])
    @validator()
    def put(self, id=None):
        logged_in_user = User.get_current_user()
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        user_obj = User.get_by_id(id)
        password = None
        if not user_obj:
            result = dict(message="User not found.")
            return self.response(result)
        if 'old_password' and 'new_password' in request.json:
            if request.json.get('old_password') and request.json.get(
                    'new_password'):
                confirm_password = password_helper.check_password_hash(
                    user_obj.password, request.json.get('old_password'))
                if not confirm_password:
                    app.logger.warning(
                        '{} submitted password which does '
                        'not match existing password'
                            .format(logged_in_user.get_full_name))
                    return {
                               "message": "Old password does not "
                                          "match existing password"
                           }, 400
                password = password_helper.generate_password_hash(
                    request.json.get('new_password'),
                    app.config.get('BCRYPT_LOG_ROUNDS')
                )
        user_obj.first_name = request.json.get(
            'first_name') if request.json.get(
            'first_name') else user_obj.first_name
        user_obj.last_name = request.json.get(
            'last_name') if request.json.get(
            'last_name') else user_obj.last_name
        user_obj.email = request.json.get('email') if request.json.get(
            'email') else user_obj.email
        user_obj.phone = request.json.get('phone') if request.json.get(
            'phone') else user_obj.email
        user_obj.password = password if password else user_obj.password
        user_obj.save()
        result = dict(message="Successfully updated record!")
        return self.response(result, 201)


class OnlineStatusApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        users = User.get_online_users()
        if users:
            return self.response(users)
        result = dict(count=0, results=[])
        return self.response(result)


class DownloadUserApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self):
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(
            ['id', 'first_name', 'last_name', 'phone', 'email', 'roles',
             'created_at', 'updated_at'])
        users = User.query.order_by(desc(User.created_at)).all()
        for obj in users:
            cw.writerow(
                [obj.id, obj.first_name, obj.last_name, obj.phone,
                 obj.email,
                 [user_role.role.name for user_role in obj.roles],
                 obj.created_at, obj.updated_at])
        output = make_response(si.getvalue())
        output.headers[
            "Content-Disposition"] = "attachment; filename={}_{}.csv".format(
            "all_users", datetime.now())
        output.headers["Content-type"] = "text/csv"
        si.close()
        return output
