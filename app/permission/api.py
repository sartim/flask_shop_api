from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.api import BaseResource
from app.core.helpers.decorators import validate, content_type
from app.permission.models import Permission


class PermissionApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, permission_id=None):
        page = request.args.get('page')
        if permission_id:
            result = Permission.get_by_id(permission_id)
            return self.response(**result)
        roles = Permission.get_all_data(int(page) if page else None)
        return self.response(roles)

    @validate(['name'])
    @content_type(['application/json'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        role = Permission(**request.json)
        role.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, permission_id=None):
        role = Permission.get_by_id(permission_id)
        if not role:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Permission.update(id, **request.json)
        if not updated:
            result = dict(message="Did not update role.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, permission_id=None):
        role = Permission.get_by_id(permission_id)
        if not role:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = role.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(permission_id))
            return self.response(result)
        result = dict(message="{} Not deleted".format(permission_id))
        return self.response(result, 400)
