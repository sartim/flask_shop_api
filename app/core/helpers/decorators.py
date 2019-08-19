from functools import wraps
from flask import request

from app.core.api import BaseResource
from app.core.helpers import validator


def validate(keys, fn=None):
    """
    Validates fields submitted with request
    :param keys:
    :param fn:
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            request_body = request.form.to_dict()
            if request.is_json:
                request_body = request.get_json()
            validated = validator.field_validator(keys, request_body)
            if not validated["success"]:
                return BaseResource.response(validated['data'], 400)
            resp = func(*args, **kwargs)
            return resp
        return inner
    return wrapper(fn) if fn else wrapper


def content_type(keys, fn=None):
    """
    Checks the content type header sent
    :param keys:
    :param fn:
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not request.content_type in keys:
                result = dict(message='Content type header is not {}'.format(keys[0]))
                return BaseResource.response(result, 400)
            resp = func(*args, **kwargs)
            return resp
        return inner
    return wrapper(fn) if fn else wrapper
