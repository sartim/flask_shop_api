from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from app.core.api import BaseResource
from app.core.helpers.decorators import validate
from app.status.models import Status


class StatusApi(BaseResource):
    decorators = [cross_origin(), jwt_required]

    def get(self, status_id=None):
        page = request.args.get('page')
        if status_id:
            result = Status.get_by_id(status_id)
            return self.response(**result)
        statuses = Status.get_all_data(int(page) if page else None)
        return self.response(statuses)

    @validate(['name'])
    def post(self):
        if not request.is_json:
            result = dict(message='Content type not json')
            return self.response(result, 400)
        status = Status(**request.json)
        status.create()
        result = dict(message="Successfully Saved!")
        return self.response(result, 201)

    def put(self, status_id=None):
        status = Status.get_by_id(status_id)
        if not status:
            result = dict(message="Id not found")
            return self.response(result, 404)
        updated = Status.update(status_id, **request.json)
        if not updated:
            result = dict(message="Did not update order status.")
            return self.response(result, 400)
        result = dict(message="Successfully Updated!")
        return self.response(result, 201)

    def delete(self, status_id=None):
        status = Status.get_by_id(status_id)
        if not status:
            result = dict(message="Id not found")
            return self.response(result, 404)
        result = status.delete()
        if result:
            result = dict(message="Successfully deleted {}".format(status_id))
            return self.response(result)
        result = dict(message="{} Not deleted".format(status_id))
        return self.response(result, 400)
