import csv

from datetime import datetime
from io import StringIO
from flask import request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import (jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity)
from sqlalchemy import desc
from app import app
from app.core.api import BaseResource
from app.core.constants import Message
from app.core.helpers import utils
from app.core.helpers.decorators import validate
from app.role.models import Role
from app.user.models import User, UserRole


class GenerateJwtApi(BaseResource):
    decorators = [cross_origin()]

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
                app.logger.info("Logged in user with the email {0}".
                                format(email))
                access_token = create_access_token(identity=email,
                                                   expires_delta=False)
                refresh_token = create_refresh_token(identity=email)
                result = dict(access_token=access_token,
                              refresh_token=refresh_token,
                              user=dict(
                                  id=user.id,
                                  full_name="{} {}".format(user.first_name,
                                                           user.last_name,
                                                           email=user.email),
                                  roles=[user_role.role.name for user_role in user.roles]))
                return self.response(result)
            else:
                app.logger.warning("User with the email {0} does not exist".
                                   format(email))
                result = dict(message="Bad username or password")
                return self.response(result, 401)
        else:
            app.logger.warning("User with the email {0} does not exist".
                               format(email))
            result = dict(message="Bad username or password")
            return self.response(result, 401)


class RefreshJwtApi(BaseResource):
    decorators = [cross_origin(), jwt_refresh_token_required]

    def post(self):
        current_user = get_jwt_identity()
        result = dict(access_token=create_access_token(identity=current_user))
        return self.response(result)


class UserApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, user_id=None):
        page = request.args.get('page')
        if user_id is None:
            users = User.get_all_data(int(page) if page else None)
            return self.response(users)
        user = User.get_by_id_data(user_id)
        return self.response(user)

    @validate(['first_name', 'last_name', 'email', 'phone', 'password', 'roles'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        body = request.json
        roles = request.json.get('roles')
        del body['roles']
        user_obj = User(**body).create()
        for role in roles:
            user_obj.roles.append(UserRole(user_obj, Role.get_by_name(role).id))
            user_obj.save()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

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
            if request.json.get('old_password') and request.json.get('new_password'):
                confirm_password = utils.check_password_hash(
                    user_obj.password, request.json.get('old_password'))
                if not confirm_password:
                    app.logger.warning('{} submitted password which does '
                                       'not match existing password'
                                       .format(logged_in_user.get_full_name))
                    return {
                               "message": "Old password does not match existing password"
                           }, 400
                password = utils.generate_password_hash(request.json.get('new_password'),
                                                        app.config.get('BCRYPT_LOG_ROUNDS'))
        user_obj.first_name = request.json.get('first_name') if request.json.get('first_name') else user_obj.first_name
        user_obj.middle_name = request.json.get('middle_name') if request.json.get(
            'middle_name') else user_obj.middle_name
        user_obj.last_name = request.json.get('last_name') if request.json.get('last_name') else user_obj.last_name
        user_obj.email = request.json.get('email') if request.json.get('email') else user_obj.email
        user_obj.phone = request.json.get('phone') if request.json.get('phone') else user_obj.email
        user_obj.password = password if password else user_obj.password
        user_obj.save()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def delete(self, id=None):
        logged_in_user = User.get_current_user()
        user = User.get_by_id(id)
        if user:
            try:
                user.delete()
                user.save()
                app.logger.debug("Successfully deleted user with id {}".format(id))
                result = dict(message=Message.SUCCESS)
                return self.response(result, 204)
            except Exception as e:
                app.logger.exception('Exception occurred. Made by {}'.format(logged_in_user.name))
                result = dict(message='An error occurred. {}'.format(str(e)))
                return self.response(result, 400)
        app.logger.warning('{} trying to delete user with id {} who does not exist'.
                           format(logged_in_user.name, id))
        result = dict(message="User with id {} does not exist".format(id))
        return self.response(result, 404)


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
        cw.writerow(['id', 'first_name', 'last_name', 'phone', 'email', 'roles', 'created_at', 'updated_at'])
        users = User.query.order_by(desc(User.created_at)).all()
        for obj in users:
            cw.writerow([obj.id, obj.first_name, obj.last_name, obj.phone, obj.email,
                         [user_role.role.name for user_role in obj.roles], obj.created_at, obj.updated_at])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename={}_{}.csv".format("all_users", datetime.now())
        output.headers["Content-type"] = "text/csv"
        si.close()
        return output


class RoleApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, id=None):
        page = request.args.get('page')
        if id:
            result = Role.get_by_id(id)
            return self.response(**result)
        roles = Role.get_all_data(int(page) if page else None)
        return self.response(**roles)

    @validate(['name'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        role = Role(**request.json)
        role.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, id=None):
        role = Role.get_by_id(id=id)
        if not role:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Role.update(id, **request.json)
        if not updated:
            result = dict(message="Did not update role.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, id=None):
        role = Role.get_by_id(id)
        if not role:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = role.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(id))
            return self.response(result)
        result = dict(message="{} Not deleted".format(id))
        return self.response(result, 400)
