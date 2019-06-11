from flask import request, jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.helpers import validator, utils
from constants import Message


class AccountView(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        logged_in_user = AccountUser.get_current_user()
        page = request.args.get('page')
        user_id = request.args.get('user_id')
        email = request.args.get('email')
        phone = request.args.get('phone')
        if user_id:
            account = AccountUser.get_by_id(user_id)
            user = AccountUser.get_user(account)
            if user:
                if user:
                    return jsonify(user)
            app.logger.warning('{} submitted {} user id which does not exist'
                               .format(logged_in_user.get_full_name, user_id))
            return jsonify(message='{} does not exist'.format(user_id))
        if email:
            account = AccountUser.get_user_by_email(email)
            user = AccountUser.get_user(account)
            if user:
                return jsonify(user)
            app.logger.warning('{} submitted {} email which does not exist'
                               .format(logged_in_user.get_full_name, email))
            return jsonify(message='{} does not exist'.format(email)), 404
        if phone:
            account = AccountUser.get_user_by_phone(phone)
            user = AccountUser.get_user(account)
            if user:
                return jsonify(user)
            app.logger.warning('{} submitted {} phone number which does not exist'
                               .format(logged_in_user.get_full_name, phone))
            return jsonify(message='{} does not exist'.format(phone)), 404
        users = AccountUser.get_all(int(page) if page else None)
        return jsonify(users)

    @cross_origin()
    def post(self):
        body = request.data
        keys = ['first_name', 'last_name', 'email', 'phone', 'password']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning('User made request with invalid fields: \n {}'.format(body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('User made request with invalid fields: \n {}'.format(body))
                return jsonify(validated['data'])
            first_name = body['first_name']
            middle_name = body['middle_name'] if 'middle_name' in body else None
            last_name = body['last_name']
            email = body['email']
            phone = body['phone']
            password = utils.generate_password_hash(body['password'], app.config.get('BCRYPT_LOG_ROUNDS'))
            user_by_email = AccountUser.get_user_by_email(email=email)
            if user_by_email:
                message = 'User with the email {} exists'.format(email)
                app.logger.warning(message)
                return jsonify(message=message), 400
            user_by_phone = AccountUser.get_user_by_phone(phone=phone)
            if user_by_phone:
                message = 'User with the phone {} exists'.format(phone)
                app.logger.warning(message)
                return jsonify(message=message), 400
            try:
                account_user = AccountUser(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                           email=email, phone=phone, password=password)
                account_user = account_user.create(account_user)
                account_user.save()
                AccountUserRole.get_or_create(account_user.id, ['CLIENT'])
                app.logger.debug("Successfully saved new user")
                return jsonify(message="Successfully saved new user"), 201
            except Exception as e:
                app.logger.exception('Exception occurred')
                return jsonify(message='An error occurred. {}'.format(str(e))), 400
        else:
            app.logger.warning('User submitted request with content type header not being application/json')
            return jsonify(message='Content-type header is not application/json'), 400

    @cross_origin()
    @jwt_required
    def put(self):
        logged_in_user = AccountUser.get_current_user()
        body = request.data
        keys = ['id']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning('{logged_in_user} made request with invalid fields: \n {request_body}'
                                   .format(logged_in_user=logged_in_user.get_full_name, request_body=body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('{} made request with invalid fields: \n {}'
                                   .format(logged_in_user.get_full_name, body))
                return jsonify(validated['data']), 400
            account_user = AccountUser.get_by_id(body['id'])
            if account_user:
                first_name = body['first_name'] if 'first_name' in body else None
                middle_name = body['middle_name'] if 'middle_name' in body else None
                last_name = body['last_name'] if 'last_name' in body else None
                email = body['email'] if 'email' in body else None
                phone = body['phone'] if 'phone' in body else None
                password = None
                if 'old_password' and 'new_password' in body:
                    if body['old_password'] and body['new_password']:
                        confirm_password = utils.check_password_hash(account_user.password, body['old_password'])
                        if not confirm_password:
                            app.logger.warning('{} submitted password which does not match existing password'
                                               .format(logged_in_user.get_full_name))
                            return jsonify(message='Old password does not match existing password'), 400
                    password = utils.generate_password_hash(body['new_password'], app.config.get('BCRYPT_LOG_ROUNDS'))
                user_by_email = AccountUser.get_user_by_email(email=email)
                if user_by_email:
                    message = 'User with the email {} exists'.format(email)
                    app.logger.warning(message)
                    return jsonify(message=message), 400
                user_by_phone = AccountUser.get_user_by_phone(phone=phone)
                if user_by_phone:
                    message = 'User with the phone {} exists'.format(phone)
                    app.logger.warning(message)
                    return jsonify(message=message), 400
                try:
                    if account_user.id == logged_in_user.id:
                        account_user.first_name = first_name if first_name else account_user.first_name
                        account_user.middle_name = middle_name if middle_name else account_user.middle_name
                        account_user.last_name = last_name if last_name else account_user.last_name
                        account_user.email = email if email else account_user.email
                        account_user.phone = phone if phone else account_user.phone
                        account_user.password = password if password else account_user.password
                        account_user.save()
                        app.logger.debug("Successfully updated my user profile with the details: \n{}".format(body))
                        return jsonify(message=Message.SUCCESS), 201
                except Exception as e:
                    app.logger.exception('Exception occurred')
                    return jsonify(message='An error occurred. {}'.format(str(e))), 400
            app.logger.warning('{} trying to update user details with {} who does not exist'.
                               format(logged_in_user.get_full_name, body['id']))
            return jsonify(message='User with id {} does not exist'.format(body['id'])), 404
        else:
            app.logger.warning('User submitted request with content type header not being application/json')
            return jsonify(message='Content-type header is not application/json'), 400

    @cross_origin()
    @jwt_required
    def delete(self):
        logged_in_user = AccountUser.get_current_user()
        body = request.data
        keys = ['id']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning(
                    '{logged_in_user} made request with invalid fields: \n {request_body}'
                        .format(logged_in_user=logged_in_user.name, request_body=body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('{logged_in_user} made request with invalid fields: \n {request_body}'
                                   .format(logged_in_user=logged_in_user.name, request_body=body))
                return jsonify(validated['data']), 400
            user = AccountUser.get_by_id(body['id'])
            if user:
                try:
                    user.delete()
                    user.save()
                    app.logger.debug("Successfully deleted user with id {}".format(body['id']))
                    return jsonify(message=Message.SUCCESS), 200
                except Exception as e:
                    app.logger.exception('Exception occurred. Made by {}'.format(logged_in_user.name))
                    return jsonify(message='An error occurred. {}'.format(str(e))), 400
            app.logger.warning('{} trying to delete user with id {} who does not exist'.
                               format(logged_in_user.name, body['id']))
            return jsonify(message='User with id {} does not exist'.format(body['id'])), 404
        else:
            app.logger.warning('{} submitted request with content type header not being application/json')
            return jsonify(message='Content-type header is not application/json'), 400


app.add_url_rule('/account/user/', view_func=AccountView.as_view('account-user'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
