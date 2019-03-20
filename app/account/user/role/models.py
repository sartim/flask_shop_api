from app import db
from app.account.role.models import AccountRole


class AccountUserRole(db.Model):

    __tablename__ = 'account_user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('account_roles.id'), primary_key=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('AccountUser', backref='account_user', lazy=True)
    role = db.relationship(AccountRole, backref='account_role', lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)
