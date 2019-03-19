from app import db

class AccountUserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pass