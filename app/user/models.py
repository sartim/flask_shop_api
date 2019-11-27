from flask_jwt_extended import get_jwt_identity

from app.core.models import BaseModel
from app import db, app


class User(BaseModel):
    __tablename__ = 'user'

    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    image = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=False)

    roles = db.relationship('UserRole',
                            cascade="save-update, merge, delete",
                            lazy=True)
    sessions = db.relationship('UserAuthenticated',
                               backref='user_sessions',
                               cascade="save-update, merge, ""delete",
                               lazy=True)
    expenses = db.relationship('Expense', backref='user_expenses', lazy=True)

    def __init__(self, first_name=None, middle_name=None, last_name=None,
                 email=None, phone=None, password=None, token=None, image=None,
                 is_active=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.token = token
        self.image = image
        self.is_active = is_active

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.id)

    @property
    def get_logged_in_id(self):
        email = get_jwt_identity()
        user = self.get_user_by_email(email)
        return user.id

    @property
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def get_online_users(cls):
        sessions = UserAuthenticated.get_all()
        if sessions:
            results = []
            for session in sessions:
                user = User.get_by_id(session.user_id)
                results.append({"id": user.id, "name": "{} {}".
                               format(user.first_name, user.last_name)})
            data = {"count": len(results), "results": results}
            return data
        return None

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()


class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User', lazy=True)
    role = db.relationship('Role', lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)

    @classmethod
    def get_or_create(cls, user_id, roles):
        for r in roles:
            role = UserRole.get_by_name(r)
            cls.create(UserRole(user_id, role.id))

    def create(self):
        try:
            db.session.add(self)
            self.save()
            return self
        except Exception as e:
            app.logger.exception("Error creating object - {}. {}".format(self.__name__, str(e)))
            return False

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))


class UserAuthenticated(db.Model):
    __tablename__ = 'user_authenticated'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    session_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, user_id=None, session_id=None):
        self.user_id = user_id
        self.session_id = session_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)

    @classmethod
    def get_by_session_id(cls, sid):
        return cls.query.filter_by(session_id=sid).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

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
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))