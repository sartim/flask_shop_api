from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.api import BaseResource
from app.core.helpers.decorators import validate
from app.role.models import Role


class RoleApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, role_id=None):
        page = request.args.get('page')
        if role_id:
            result = Role.get_by_id(role_id)
            return self.response(**result)
        roles = Role.get_all_data(int(page) if page else None)
        return self.response(roles)

    @validate(['name'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        role = Role(**request.json)
        role.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, role_id=None):
        role = Role.get_by_id(role_id)
        if not role:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Role.update(role_id, **request.json)
        if not updated:
            result = dict(message="Did not update role.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, role_id=None):
        role = Role.get_by_id(role_id)
        if not role:
            result = dict(message="Role id not found")
            return self.response(result, 404)
        result = role.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(id))
            return self.response(result)
        result = dict(message="{} Not deleted".format(id))
        return self.response(result, 400)
