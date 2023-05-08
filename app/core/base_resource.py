from typing import TypedDict

from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app import app, parser
from app.core.constants import ResponseMessage
from app.core.helpers.decorators import (
    content_type, validator, check_permission)
from app.core.redis import redis


class BaseResource(MethodView):
    decorators = [cross_origin(), jwt_required()]
    model = None
    schema = None
    request_args = None

    @check_permission()
    def get(self, _id=None):
        endpoint = request.endpoint[:-4].upper()
        if _id:
            obj = self.model.get_by_id(_id, **dict(endpoint=endpoint))
            if obj.deleted:
                result = dict(message=ResponseMessage.RECORD_ALREADY_DELETED)
                app.logger.warning("Record {} retrieval error. {}".format(
                    _id, result))
                return self.response(result, 410)
            result = obj.to_dict(self.schema, obj)
            return self.response(result)
        params = parser.parse(self.request_args, request, location='querystring')
        id_list = request.args.getlist("id")
        ids = None
        if len(id_list) > 1:
            del params["id"]
            ids = id_list
        params.update(endpoint=endpoint)
        if "deleted" not in params:
            params.update(deleted=False)
        results = self.model.get_all_data(self.schema, ids, **params)
        return self.response(results)

    @content_type(['application/json'])
    @validator()
    @check_permission()
    def post(self):
        data = request.json
        try:
            self.schema().load(request.json)
        except ValidationError as err:
            app.logger.warning("Record validation error. {}".format(
                err.messages))
            return err.messages, 400
        is_created, msg = self.model(**data).create()
        if not is_created:
            result = dict(
                message=msg if msg else ResponseMessage.RECORD_NOT_SAVED)
            app.logger.warning("Record {} creation error. {}".format(
                request.json, result)
            )
            return self.response(result, 400)
        self.delete_cached_query()
        result_data = self.model.to_dict(self.schema, is_created)
        result = dict(
            message=ResponseMessage.RECORD_SAVED,
            data=result_data)
        return self.response(result, 201)

    @content_type(['application/json'])
    @validator()
    @check_permission()
    def put(self, _id):
        endpoint = request.endpoint[:-4].upper()
        obj = self.model.get_by_id(_id, **dict(endpoint=endpoint))
        data = request.json
        if obj.deleted:
            result = dict(ResponseMessage.RECORD_ALREADY_DELETED)
            app.logger.warning("Record {} update error. {}".format(
                _id, result))
            return self.response(result, 410)
        updated = self.model.update(_id, **data)
        if not updated:
            result = dict(message=ResponseMessage.RECORD_NOT_UPDATED)
            app.logger.warning("Record {} update error. {}".format(
                _id, result))
            return self.response(result, 400)
        self.delete_cached_query()
        result_data = obj.to_dict(self.schema, obj)
        result = dict(
            message=ResponseMessage.RECORD_UPDATED,
            data=result_data
        )
        return self.response(result, 200)

    @check_permission()
    def delete(self, _id):
        endpoint = request.endpoint[:-4].upper()
        obj = self.model.get_by_id(_id, **dict(endpoint=endpoint))
        delete_type = request.args.get("delete_type")
        if obj.deleted:
            result = dict(message=ResponseMessage.RECORD_ALREADY_DELETED)
            app.logger.warning("Record {} retrieval error. {}".format(
                _id, result))
            return self.response(result, 410)
        if delete_type == "soft":
            obj.deleted = True
            result, msg = obj.save()
        else:
            result, msg = obj.delete()
        if result:
            self.delete_cached_query()
            return self.response(
                dict(message=ResponseMessage.RECORD_DELETED), 200)
        result = dict(message=ResponseMessage.RECORD_NOT_DELETED)
        app.logger.warning("Record {} deletion error. {}".format(
            _id, result))
        return self.response(result, 400)

    @staticmethod
    def response(payload=None, status=200):
        return jsonify(payload), status

    @staticmethod
    def delete_cached_query():
        redis.delete(app.config.get("CACHED_QUERY"))


class ChildBaseResource(BaseResource):
    field = None
    parent = None

    @check_permission()
    def get(self, _id=None):
        endpoint = request.endpoint[:-4].upper()
        if _id:
            obj = self.parent.get_by_id(_id, **dict(endpoint=endpoint))
            if obj.deleted:
                return self.response(ResponseMessage.RECORD_ALREADY_DELETED,
                                     410)
            params = {}
            if self.request_args:
                params = parser.parse(
                    self.request_args, request, location='querystring')
            params["" + self.field + ""] = _id
            params.update(endpoint=endpoint)
            results = self.model.get_all_data(self.schema, None, **params)
            return self.response(results)
        results = dict(message="Record not found.")
        app.logger.warning("Record {} retrieval error. {}".format(_id, results))
        return self.response(results, 404)

    @check_permission()
    @content_type(['application/json'])
    @validator()
    def put(self, _id):
        endpoint = request.endpoint[:-4].upper()
        data = request.json
        try:
            self.schema().load(data)
        except ValidationError as err:
            result = jsonify(err.messages)
            app.logger.warning("Record {} validation error. {}".format(
                data, result))
            return result, 400
        if self.parent.get_by_id(_id, endpoint=endpoint):
            data["" + self.field] = _id
            is_created, msg = self.model(**data).create()
            if not is_created:
                result = dict(
                    message=msg if msg else ResponseMessage.RECORD_NOT_SAVED)
                app.logger.warning("Record creation error. {}".format(result))
                return self.response(result, 400)
            self.delete_cached_query()
            result = dict(message=ResponseMessage.RECORD_SAVED)
            return self.response(result, 201)
        result = dict(message=ResponseMessage.RECORD_NOT_SAVED)
        app.logger.warning("Record {} creation error. {}".format(data, result))
        return self.response(result, 400)

    @check_permission()
    def delete(self, _id):
        params = request.args.to_dict()
        if not params:
            return self.response(
                dict(message=ResponseMessage.PROVIDE_DELETE_PARAMETERS), 200)
        params[str(self.field)] = _id
        obj = self.model.filter_by(**params)
        if not obj:
            return self.response(
                dict(message=ResponseMessage.RECORD_NOT_FOUND), 404)
        is_deleted, msg = self.model.delete(obj)
        if is_deleted:
            self.delete_cached_query()
            return self.response(
                dict(message=ResponseMessage.RECORD_DELETED), 200)
        result = dict(message=ResponseMessage.RECORD_NOT_DELETED)
        app.logger.warning("Record {} deletion error. {}".format(_id, result))
        return self.response(result, 400)
