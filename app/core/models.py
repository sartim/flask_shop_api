from datetime import date, datetime

import flask
import os

from flask_jwt_extended import get_jwt_identity
from sqlalchemy import desc, func, extract

from app import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    @classmethod
    def get_dict(cls, **kwargs):
        return dict(kwargs)

    @classmethod
    def response(cls, obj):
        data = obj.__dict__
        del data['_sa_instance_state']
        return data

    @classmethod
    def get_by_id_data(cls, _id):
        obj = cls.get_by_id(_id)
        data = cls.response(obj)
        return data

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id) \
            .first_or_404(description='No result found')

    @classmethod
    def get_current_user(cls):
        return cls.query \
            .filter_by(email=get_jwt_identity()).first()

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

    def create(self):
        try:
            db.session.add(self)
            self.save()
        except Exception as e:
            app.logger.exception("Error creating object - {}. {}"
                                 .format(self.__name__, str(e)))
            return False
        return self

    @classmethod
    def get_or_create(cls, **kwargs):
        obj = cls.query.filter_by(**kwargs).first()
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

    def delete(self):
        try:
            db.session.delete(self)
            return True
        except Exception:
            app.logger.exception(
                'Could not delete {} instance.'.format(self.__name__))
        return False

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'
                             .format(cls.__name__))
        except Exception:
            app.logger.exception(
                'Exception occurred. Could not save {} instance.'
                    .format(cls.__name__)
            )

    @classmethod
    def revert(cls):
        return db.session.rollback()

    @classmethod
    def build_response(cls, obj, results, path, _id=None, **kwargs):
        domain = flask.request.url_root
        prev_url, next_url = None, None
        if _id:
            next_url = "{}{}?id={}".format(domain, path, _id)
        elif kwargs:
            next_url = "{}{}?{}={}&page={}".format(
                domain, path, ' '.join(kwargs.keys()),
                kwargs[' '.join(kwargs.keys())],
                obj.next_num
            )
        elif not _id:
            next_url = "{}{}?page={}".format(
                domain, path, obj.next_num
            )

        if kwargs:
            prev_url = "{}{}?{}={}&page={}".format(
                domain, path,
                ' '.join(kwargs.keys()),
                kwargs[' '.join(kwargs.keys())],
                obj.prev_num
            )
        elif not _id:
            prev_url = "{0}{1}?page={2}".format(
                domain, path, obj.prev_num
            )
        elif _id:
            prev_url = "{}{}?id={}&page={}".format(
                domain, path, _id, obj.prev_num,
                domain, path, _id, obj.prev_num
            )

        if obj.has_next:
            data = dict(
                count=obj.total, results=results, next=next_url,
                previous=prev_url if obj.prev_num else ""
            )
        else:
            data = dict(
                count=obj.total, results=results, next="", previous=""
            )
        return data

    @classmethod
    def get_all(cls, page):
        query = cls.query.order_by(desc(cls.created_at))
        results = cls.paginate_result(query, page)
        return results

    @classmethod
    def get_all_data(cls, page):
        objects = cls.get_all(page)
        return cls.build_paginated_response(
            objects, flask.request.full_path
        )

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

    @classmethod
    def paginate_result(cls, query, page):
        return query.paginate(
            page=page,
            per_page=int(os.environ.get('PAGINATE_BY')),
            error_out=True
        )

    @classmethod
    def build_paginated_response(cls, objects, url):
        results = []
        for obj in objects.items:
            data = cls.response(obj)
            results.append(data)
        data = cls.build_response(objects, results, url)
        return data
