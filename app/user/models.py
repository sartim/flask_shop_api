from flask_jwt_extended import get_jwt_identity
from app.core.base_model import BaseModel, AbstractBaseModel
from app.core.app import db, app
from sqlalchemy import text, desc, asc
from sqlalchemy.dialects.postgresql import UUID
from app.permission.models import Permission
from app.role.models import RolePermission


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
    deleted = db.Column(db.Boolean, default=False)

    roles = db.relationship(
        "UserRole", cascade="save-update, merge, delete", lazy=False
    )
    sessions = db.relationship(
        "UserAuthenticated", backref='user_sessions',
        cascade="save-update, merge, ""delete", lazy=False
    )

    def __init__(
            self, id=None, first_name=None, middle_name=None,
            last_name=None, email=None, phone=None, password=None,
            token=None, image=None, is_active=None, deleted=None):
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
        self.deleted = deleted

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.id)

    def get_logged_in_id(self):
        email = get_jwt_identity()
        user = self.get_user_by_email(email)
        if user:
            return str(user.id)
        return None

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def has_permission(cls, permission):
        user = cls.get_current_user()
        permission_obj = Permission.get_by_name(permission)
        if permission_obj and user:
            perm = UserPermission.filter_by(
                permission_id=permission_obj.id, user_id=user.id)
            if not perm:
                for role in user.roles:
                    perm = RolePermission.filter_by(
                        role_id=role.role_id, permission_id=permission_obj.id
                    )
                    if perm:
                        break
                if perm:
                    return perm
        else:
            app.logger.warning(
                "Permissions {} does not exist.".format(permission))
        return False

    @classmethod
    def get_curr_user_roles(cls):
        curr_user = cls.get_current_user()
        return [r.role.id for r in curr_user.roles]

    @classmethod
    def get_by_id(cls, _id, **kwargs):
        if User.check_has_view_permission(kwargs["endpoint"]):
            return cls.query.filter_by(id=_id) \
                .first_or_404(description="Record not found.")
        elif User.check_has_belonging_view_permission(kwargs["endpoint"]):
            return cls.query.filter_by(id=cls.get_current_user().id) \
                .first_or_404(description="Record not found.")

    @classmethod
    def get_all(cls, **kwargs):
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
        if "role_id" in kwargs:
            query = cls.get_all_with_role(kwargs["role_id"])
        else:
            query = cls.query.filter_by(**kwargs).order_by(
                desc(cls.created_at))

        if start_created_at and end_created_at:
            query = query.filter(cls.created_at <= end_created_at). \
                filter(cls.created_at >= start_created_at)
        if start_updated_at and end_updated_at:
            query = query.filter(cls.updated_at <= end_updated_at). \
                filter(cls.updated_at >= start_updated_at)

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

    @classmethod
    def get_all_with_role(cls, role_id):
        usr_on_role = UserRole.query.filter(
            UserRole.role_id == role_id).all()
        usr_ids = (v.user_id for v in usr_on_role)
        return User.query.filter(cls.id.in_(usr_ids)).order_by(
            desc(cls.created_at))


class UserRole(db.Model):
    __tablename__ = "user_role"

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), primary_key=True
    )
    role_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("role.id"), primary_key=True
    )
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    user = db.relationship("User", lazy=True, overlaps="roles")
    role = db.relationship("Role", lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "<%r (%r)" % (self.__class__.__name__, self.user_id)


class UserAuthenticated(db.Model):
    __tablename__ = "user_authenticated"

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), primary_key=True
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


class UserPermission(AbstractBaseModel):
    __tablename__ = 'user_permission'

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.id'), primary_key=True)
    permission_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('permission.id'), primary_key=True
    )

    user = db.relationship('User', lazy=False)
    permission = db.relationship('Permission', lazy=False)

    def __init__(self, user_id=None, permission_id=None):
        self.user_id = user_id
        self.permission_id = permission_id

    def __repr__(self):
        return "<%r (%r)>" % (self.__class__.__name__, self.name)
