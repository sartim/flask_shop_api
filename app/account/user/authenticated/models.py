from app import db


class AccountUserAuthenticated(db.Model):

    __tablename__ = 'account_user_authenticated'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    session_id = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, user_id=None, session_id=None):
        self.user_id = user_id
        self.session_id = session_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)


    def get_by_session_id(cls, sid):
        return cls.query.filter_by(session_id=sid).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
