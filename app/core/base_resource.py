from flask import jsonify, request
from flask.views import MethodView

from app.core.constants import (
    RECORD_NOT_SAVED, RECORD_SAVED,
    RECORD_NOT_UPDATED, RECORD_UPDATED,
    RECORD_DELETED, RECORD_NOT_DELETED,
    RECORD_ALREADY_DELETED)
from app.core.helpers.decorators import content_type, validator


class BaseResource(MethodView):
    model = None
    schema = None

    def get(self, id=None):
        if id:
            obj = self.model.get_by_id(id)
            if obj.deleted:
                return self.response(RECORD_ALREADY_DELETED, 410)
            result = obj.to_dict(self.schema, obj)
            return self.response(result)
        params = request.args.to_dict()
        results = self.model.get_all_data(self.schema, **params)
        return self.response(results)

    @content_type(['application/json'])
    @validator(schema)
    def post(self):
        is_created, msg = self.model(**request.json).create()
        if not is_created:
            result = dict(message=msg if msg else RECORD_NOT_SAVED)
            return self.response(result, 400)
        result = dict(message=RECORD_SAVED)
        return self.response(result, 201)

    @content_type(['application/json'])
    @validator()
    def put(self, id=None):
        obj = self.model.get_by_id(id)
        if obj.deleted:
            return self.response(RECORD_ALREADY_DELETED, 410)
        updated = self.model.update(id, **request.json)
        if not updated:
            result = dict(message=RECORD_NOT_UPDATED)
            return self.response(result, 400)
        result = dict(message=RECORD_UPDATED)
        return self.response(result, 200)

    def delete(self, id=None):
        obj = self.model.get_by_id(id)
        delete_type = request.args.get("delete_type")
        if obj.deleted:
            return self.response(RECORD_ALREADY_DELETED, 410)
        if delete_type == "soft":
            obj.deleted = True
            result = obj.save()
        else:
            result = obj.delete()
        if result:
            return self.response(
                dict(message=RECORD_DELETED.format(id)), 200)
        return self.response(
            dict(message=RECORD_NOT_DELETED.format(id)), 400)

    @staticmethod
    def response(payload=None, status=200):
        return jsonify(payload), status
