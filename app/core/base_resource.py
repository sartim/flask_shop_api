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
from app.user.models import User


class BaseResource(MethodView):
    decorators = [cross_origin(), jwt_required()]
    model = None
    schema = None
    request_args = None

    @check_permission()
    async def get(self, _id=None):
        endpoint = request.endpoint[:-4].upper()
        if _id:
            obj = await self.model.get_by_id(_id, **dict(endpoint=endpoint))
            if obj.deleted:
                result = dict(message=ResponseMessage.RECORD_ALREADY_DELETED)
                app.logger.warning("Record {} retrieval error. {}".format(
                    _id, result))
                return self.response(result, 410)
            result = await obj.to_dict(self.schema, obj)
            return await self.response(result)
        params = parser.parse(self.request_args, request, location='querystring')
        id_list = request.args.getlist("id")
        ids = None
        if len(id_list) > 1:
            del params["id"]
            ids = id_list
        params.update(endpoint=endpoint)
        if "deleted" not in params:
            params.update(deleted=False)
        results = await self.model.get_all_data(self.schema, ids, **params)
        return await self.response(results)

    @content_type(['application/json'])
    @validator()
    @check_permission()
    async def post(self):
        data = request.json
        try:
            self.schema().load(request.json)
        except ValidationError as err:
            app.logger.warning("Record validation error. {}".format(
                err.messages))
            return err.messages, 400
        is_created, msg = await self.model(**data).create()
        if not is_created:
            result = dict(
                message=msg if msg else ResponseMessage.RECORD_NOT_SAVED)
            app.logger.warning("Record {} creation error. {}".format(
                request.json, result)
            )
            return await self.response(result, 400)
        await self.delete_cached_query()
        result_data = await self.model.to_dict(self.schema, is_created)
        result = dict(
            message=ResponseMessage.RECORD_SAVED,
            data=result_data)
        return await self.response(result, 201)

    @content_type(['application/json'])
    @validator()
    @check_permission()
    async def put(self, _id):
        endpoint = request.endpoint[:-4].upper()
        obj = await self.model.get_by_id(_id, **dict(endpoint=endpoint))
        data = request.json
        if obj.deleted:
            result = dict(ResponseMessage.RECORD_ALREADY_DELETED)
            app.logger.warning("Record {} update error. {}".format(
                _id, result))
            return await self.response(result, 410)
        updated = await self.model.update(_id, **data)
        if not updated:
            result = dict(message=ResponseMessage.RECORD_NOT_UPDATED)
            app.logger.warning("Record {} update error. {}".format(
                _id, result))
            return await self.response(result, 400)
        await self.delete_cached_query()
        result_data = await obj.to_dict(self.schema, obj)
        result = dict(
            message=ResponseMessage.RECORD_UPDATED,
            data=result_data
        )
        return await self.response(result, 200)

    @check_permission()
    async def delete(self, _id):
        endpoint = request.endpoint[:-4].upper()
        obj = self.model.get_by_id(_id, **dict(endpoint=endpoint))
        delete_type = request.args.get("delete_type")
        if obj.deleted:
            result = dict(message=ResponseMessage.RECORD_ALREADY_DELETED)
            app.logger.warning("Record {} retrieval error. {}".format(
                _id, result))
            return await self.response(result, 410)
        if delete_type == "soft":
            obj.deleted = True
            result, msg = await obj.save()
        else:
            result, msg = await obj.delete()
        if result:
            await self.delete_cached_query()
            return await self.response(
                dict(message=ResponseMessage.RECORD_DELETED), 200)
        result = dict(message=ResponseMessage.RECORD_NOT_DELETED)
        app.logger.warning("Record {} deletion error. {}".format(
            _id, result))
        return await self.response(result, 400)

    @staticmethod
    async def response(payload=None, status=200):
        return jsonify(payload), status

    @staticmethod
    async def delete_cached_query():
        redis.delete(app.config.get("CACHED_QUERY"))


class ChildBaseResource(BaseResource):
    field = None
    parent = None

    @check_permission()
    async def get(self, _id=None):
        endpoint = request.endpoint[:-4].upper()
        if _id:
            obj = await self.parent.get_by_id(_id, **dict(endpoint=endpoint))
            if obj.deleted:
                return self.response(ResponseMessage.RECORD_ALREADY_DELETED,
                                     410)
            params = {}
            if self.request_args:
                params = parser.parse(
                    self.request_args, request, location='querystring')
            params["" + self.field + ""] = _id
            params.update(endpoint=endpoint)
            results = await self.model.get_all_data(self.schema, None, **params)
            return self.response(results)
        results = dict(message="Record not found.")
        app.logger.warning("Record {} retrieval error. {}".format(_id, results))
        return self.response(results, 404)

    @check_permission()
    @content_type(['application/json'])
    @validator()
    async def put(self, _id):
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
            is_created, msg = await self.model(**data).create()
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
    async def delete(self, _id):
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
