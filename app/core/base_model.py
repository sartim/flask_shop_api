from typing import TypedDict

import flask
import sqlalchemy

from datetime import date, datetime
from flask import request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import desc, func, extract, asc
from app import db, app
from app.core.constants import ResponseMessage
from app.core.helpers import serializer
from app.core.redis import redis


class BaseModelResponse(TypedDict):
    count: int
    results: dict
    next: str
    previous: str


class AbstractBaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.current_timestamp(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=db.func.current_timestamp(),
        nullable=False, onupdate=db.func.current_timestamp()
    )

    def create(self):
        try:
            db.session.add(self)
            is_saved, msg = self.save()
            if not is_saved:
                return False, msg
        except Exception as e:
            app.logger.exception(
                "Error creating object - {}. {}"
                    .format(self.__name__, str(e))
            )
            return False, str(e)
        else:
            return self, None

    @classmethod
    def update(cls, _id, **kwargs):
        try:
            cls.query.filter(cls.id == _id) \
                .update(dict(**kwargs), synchronize_session='evaluate')
            cls.save()
        except Exception as e:
            app.logger.exception("Error occurred on update. {}"
                                 .format(str(e)))
            return False
        return True

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'
                             .format(cls.__name__))
        except sqlalchemy.exc.DBAPIError as e:
            msg = "Error code {}, {}".format(
                e.orig.pgcode, str(e.orig)
            )
            if str(e.orig.pgcode) == "23505":
                msg = str(e.orig).split(":")[1].lstrip(" ").rstrip("\n")
            app.logger.exception(msg)
            return False, msg
        except Exception as e:
            cls.revert()
            app.logger.exception(
                'Exception occurred. Could not save {} instance.'
                    .format(cls.__name__)
            )
            return False, str(e)
        else:
            return cls, None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except sqlalchemy.exc.InvalidRequestError:
            app.logger.warning(
                "Record is still referenced from table in {}"
                    .format(self)
            )
            return False, ResponseMessage.RECORD_STILL_REFERENCED
        except Exception:
            app.logger.exception(
                'Could not delete {} instance.'.format(self))
            return False, ResponseMessage.RECORD_NOT_DELETED
        else:
            return True, ResponseMessage.RECORD_DELETED

    @classmethod
    def revert(cls):
        return db.session.rollback()

    @classmethod
    def to_dict(cls, schema, obj):
        return schema().dump(obj=obj)

    @classmethod
    def build_response(cls, paginated_data, results, path, _id=None, **kwargs):
        domain = flask.request.url_root.rstrip("/")
        if app.config.get("API_GATEWAY_URL"):
            domain = app.config.get("API_GATEWAY_URL")
        prev_url, next_url = None, None
        if _id:
            next_url = "{}{}?id={}".format(domain, path, _id)
        elif kwargs:
            next_url = "{}{}?{}={}&page={}".format(
                domain, path, ' '.join(kwargs.keys()),
                kwargs[' '.join(kwargs.keys())],
                paginated_data["next_page"]
            )
        elif not _id:
            next_url = "{}{}?page={}".format(
                domain, path, paginated_data["next_page"]
            )

        if kwargs:
            prev_url = "{}{}?{}={}&page={}".format(
                domain, path,
                ' '.join(kwargs.keys()),
                kwargs[' '.join(kwargs.keys())],
                paginated_data["prev_page"]
            )
        elif not _id:
            prev_url = "{0}{1}?page={2}".format(
                domain, path, paginated_data["prev_page"]
            )
        elif _id:
            prev_url = "{}{}?id={}&page={}".format(
                domain, path, _id, paginated_data["prev_page"],
                domain, path, _id, paginated_data["prev_page"]
            )

        data: BaseModelResponse
        prev_url = prev_url if paginated_data["prev_page"] else ""
        if paginated_data["has_next"]:
            data = dict(
                count=paginated_data["total"], results=results, next=next_url,
                previous=prev_url
            )
        else:
            data = dict(
                count=paginated_data["total"], results=results, next="",
                previous=""
            )
        return data

    @classmethod
    def get_all(cls, ids, **kwargs):
        page = kwargs.get("page")
        limit = kwargs.get("limit")
        sort = kwargs.get("sort")
        sort_by = kwargs.get("sort_by", "created_at")
        start_created_at = kwargs.get("start_created_at")
        end_created_at = kwargs.get("end_created_at")
        start_updated_at = kwargs.get("start_updated_at")
        end_updated_at = kwargs.get("end_updated_at")
        if "page" in kwargs:
            del kwargs["page"]
        if "limit" in kwargs:
            del kwargs["limit"]
        if "endpoint" in kwargs:
            del kwargs["endpoint"]
        if "sort" in kwargs:
            del kwargs["sort"]
        if "sort_by" in kwargs:
            del kwargs["sort_by"]
        if "start_created_at" in kwargs:
            del kwargs["start_created_at"]
        if "end_created_at" in kwargs:
            del kwargs["end_created_at"]
        if "start_updated_at" in kwargs:
            del kwargs["start_updated_at"]
        if "end_updated_at" in kwargs:
            del kwargs["end_updated_at"]

        query = cls.query.filter_by(**kwargs)

        if start_created_at and end_created_at:
            query = query.filter(cls.created_at <= end_created_at). \
                filter(cls.created_at >= start_created_at)
        if start_updated_at and end_updated_at:
            query = query.filter(cls.updated_at <= end_updated_at). \
                filter(cls.updated_at >= start_updated_at)

        if ids:
            query = query.filter(cls.id.in_(ids))
        if not sort or sort == "desc":
            if sort_by == "create_at":
                query = query.order_by(desc(cls.created_at))
            if sort_by == "updated_at":
                query = query.order_by(desc(cls.updated_at))
        if sort == "asc":
            if sort_by == "create_at":
                query = query.order_by(asc(cls.created_at))
            if sort_by == "updated_at":
                query = query.order_by(asc(cls.updated_at))
        results = cls.paginate_result(
            query, int(page) if page else page, int(limit) if limit else limit
        )
        return results

    @staticmethod
    def paginated_result_caching(paginated_data):
        key = request.full_path
        if not redis.cache.exists(app.config.get("CACHED_QUERY")):
            redis.cache.hset(app.config.get("CACHED_QUERY"), b'na', b'na')
            redis.cache.expire(
                app.config.get("CACHED_QUERY"),
                int(app.config.get("REDIS_EXPIRE")))
        cached_result = redis.hmget_payload(
            app.config.get("CACHED_QUERY"), key
        )
        query_results = serializer.serialize(paginated_data)
        if not cached_result:
            redis.hset_payload(
                app.config.get("CACHED_QUERY"), key, query_results
            )
            return paginated_data

    @classmethod
    def get_all_data(cls, schema, ids, **kwargs):
        key = request.full_path
        cached_result = redis.hmget_payload(
            app.config.get("CACHED_QUERY"), key
        )
        if not cached_result:
            paginated_object = cls.get_all(ids, **kwargs)
            paginated_data = dict(
                next_page=paginated_object.next_num,
                prev_page=paginated_object.prev_num,
                has_next=paginated_object.has_next,
                total=paginated_object.total,
                items=paginated_object.items
            )
            paginated_data = cls.paginated_result_caching(paginated_data)
        else:
            paginated_data = serializer.deserialize(cached_result)
        return cls.build_paginated_response(
            schema, paginated_data, flask.request.path
        )

    @classmethod
    def paginate_result(cls, query, page, limit=None):
        return query.paginate(
            page=page,
            per_page=int(app.config.get("PAGINATE_BY")) if not limit else limit,
            error_out=True
        )

    @classmethod
    def build_paginated_response(cls, schema, paginated_data, url):
        results = []
        for obj in paginated_data["items"]:
            data = cls.to_dict(schema, obj)
            results.append(data)
        data = cls.build_response(paginated_data, results, url)
        return data

    @classmethod
    def get_by_id_data(cls, schema, _id):
        obj = cls.get_by_id(_id)
        data = cls.to_dict(schema, obj)
        return data

    @classmethod
    def get_by_id(cls, _id, **kwargs):
        return cls.query.filter_by(id=_id) \
            .first_or_404(description="Record not found.")

    @classmethod
    def get_current_user(cls):
        return cls.query \
            .filter_by(email=get_jwt_identity()).first().id

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.filter_by(**kwargs)
        if obj:
            return obj
        obj = cls(**kwargs)
        obj.create()
        return obj

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_or_create_by_name(cls, value):
        obj = cls.get_by_name(value)
        if obj:
            return obj
        obj = cls(value)
        obj.create()
        return obj

    @classmethod
    def filter_all_today(cls):
        return cls.query.filter(
            func.date(cls.created_at) == date.today()
        )

    @classmethod
    def filter_all_this_month(cls):
        return cls.query.filter(
            extract('month', cls.created_at) == datetime.now().month
        )

    @classmethod
    def filter_all_last_month(cls):
        return cls.query.filter(
            extract('month', cls.created_at) == datetime.now().month - 1
        )

    @classmethod
    def filter_all_this_year(cls):
        return cls.query.filter(
            extract('year', cls.created_at) == datetime.now().year
        )


class BaseModel(AbstractBaseModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
