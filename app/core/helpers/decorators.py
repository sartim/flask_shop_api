import json
from functools import wraps
from flask import request
from marshmallow import ValidationError

from app import app


def validator(schema=None, fn=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            body = request.data
            msg = "Missing request body"
            if not body:
                return dict(message=msg), 400
            if not json.loads(body):
                return dict(message=msg), 400
            request_body = request.form.to_dict()
            if request.is_json:
                if request.json:
                    request_body = request.get_json()
            if schema:
                try:
                    schema.load(request_body)
                except ValidationError as err:
                    return err.messages, 400
            resp = func(*args, **kwargs)
            return resp
        return inner
    return wrapper(fn) if fn else wrapper


def content_type(keys, fn=None):
    """Checks the content type header sent"""
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not request.content_type in keys:
                result = dict(
                    message='Content type header is not {}'.format(keys[0])
                )
                app.logger.warning(
                    'Content type header is not {}'.format(keys[0]),
                    extra={'stack': True}
                )
                return result, 400
            resp = func(*args, **kwargs)
            return resp
        return inner
    return wrapper(fn) if fn else wrapper
