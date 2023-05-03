from app.core.base_model import BaseModel
from app import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID


class User(BaseModel):
    __tablename__ = "user"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=text("uuid_generate_v4()")
    )
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    image = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=False)

    roles = db.relationship(
        "UserRole", cascade="save-update, merge, delete", lazy=True
    )
    sessions = db.relationship(
        "UserAuthenticated", backref='user_sessions',
        cascade="save-update, merge, ""delete", lazy=True
    )

    def __init__(
            self, id=None, first_name=None, middle_name=None,
            last_name=None, email=None, phone=None, password=None,
            token=None, image=None, is_active=None):
        self.id = id
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


class UserRole(db.Model):
    __tablename__ = "user_role"

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True
    )
    role_id = db.Column(
        db.Integer, db.ForeignKey("role.id"), primary_key=True
    )
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    user = db.relationship("User", lazy=True)
    role = db.relationship("Role", lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "<%r (%r)" % (self.__class__.__name__, self.user_id)


class UserAuthenticated(db.Model):
    __tablename__ = "user_authenticated"

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True
    )
    session_id = db.Column(db.String(255))
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, user_id=None, session_id=None):
        self.user_id = user_id
        self.session_id = session_id

    def __repr__(self):
        return "<%r (%r)" % (self.__class__.__name__, self.user_id)
