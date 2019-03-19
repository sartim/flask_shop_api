from flask_jwt_extended import get_jwt_identity
from app import db, app


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_current_user(cls):
        return cls.query.filter_by(email=get_jwt_identity()).first()

    @staticmethod
    def create(obj):
        db.session.add(obj)
        obj.save()
        return obj

    @classmethod
    def get_or_create(cls, value):
        obj = cls.get_by_id(value)
        if obj:
            return obj
        obj = cls(value)
        obj.create(obj)
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
        obj.create(obj)
        return obj

    def delete(self):
        try:
            db.session.delete(self)
        except Exception:
            app.logger.exception(
                'Could not delete {} instance.'.format(self.__name__))

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed AccountUser instance')
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__ ))

    @classmethod
    def revert(cls):
        """
        This reverts a failed transaction
        :return:
        """
        return db.session.rollback()
