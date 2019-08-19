import flask
import os

from sqlalchemy import desc
from app import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp(), nullable=False)

    @classmethod
    def get_dict(cls, **kwargs):
        return dict(kwargs)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first_or_404(description='No result found')

    @classmethod
    def update(cls, id, **kwargs):
        try:
            cls.query.filter(cls.id == id).update(dict(**kwargs), synchronize_session='evaluate')
            cls.save()
        except Exception as e:
            app.logger.exception("Error occurred on update. {}".format(str(e)))
            return False
        return True

    def create(self):
        db.session.add(self)
        save, message = self.save()
        return save, message, self

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
            app.logger.exception('Could not delete {} instance.'.format(self.__name__))
        return False

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception as e:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))
            return False, "Error creating object - {}. {}".format(cls.__name__, str(e))
        return True, 'Successfully committed {} instance'.format(cls.__name__)

    @classmethod
    def revert(cls):
        return db.session.rollback()

    @classmethod
    def build_response(cls, obj, results, path, id=None, **kwargs):
        domain = flask.request.url_root
        prev_url, next_url = None, None
        if id:
            next_url = "{}{}?id={}".format(domain, path, id)
        elif kwargs:
            next_url = "{}{}?{}={}&page={}".format(domain, path,
                                                   ' '.join(kwargs.keys()),
                                                   kwargs[' '.join(kwargs.keys())],
                                                   obj.next_num)
        elif not id:
            next_url = "{}{}?page={}".format(domain, path, obj.next_num)

        if kwargs:
            prev_url = "{}{}?{}={}&page={}".format(domain, path,
                                                   ' '.join(kwargs.keys()),
                                                   kwargs[' '.join(kwargs.keys())],
                                                   obj.prev_num)
        elif not id:
            prev_url = "{0}{1}?page={2}".format(domain, path, obj.prev_num)
        elif id:
            prev_url = "{}{}?id={}&page={}".format(domain, path, id, obj.prev_num)

        if obj.has_next:
            data = dict(count=obj.total, results=results, next=next_url,
                        previous=prev_url if obj.prev_num else "")
        else:
            data = dict(count=obj.total, results=results, next="", previous="")
        return data

    @classmethod
    def build_paginated_response(cls, objects, url):
        pass

    @classmethod
    def get_all(cls, page):
        objects = cls.query.order_by(desc(cls.created_at)). \
            paginate(page=page,
                     per_page=int(os.environ.get('PAGINATE_BY')),
                     error_out=True)
        return objects

    @classmethod
    def get_all_data(cls, page):
        objects = cls.get_all(page)
        return cls.build_paginated_response(objects, flask.request.full_path)
