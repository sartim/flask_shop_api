import os
import logging

from dotenv import load_dotenv
from logging.handlers import SMTPHandler
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.core.config import DevelopmentConfig, ProductionConfig, TestingConfig
from app.core.connection import elasticsearch
from webargs.flaskparser import FlaskParser

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


def create_app():
    app = Flask(__name__)
    if os.environ.get('ENV') == "DEV":
        app.config.from_object(DevelopmentConfig)
        app.elasticsearch = elasticsearch
        app.logger.debug(" * ENV: DEVELOPMENT")
    if os.environ.get('ENV') == "PROD":
        app.config.from_object(ProductionConfig)
        app.elasticsearch = elasticsearch
        app.logger.debug(" * ENV: PRODUCTION")
    if os.environ.get("ENV") == "TEST":
        app.config.from_object(TestingConfig)
        app.elasticsearch = None
        app.logger.debug(" * ENV: TESTING")
    return app

app = create_app()

parser = FlaskParser(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)
socketio = SocketIO(app)

from app.core.callbacks import *
from app.auth.routes import auth_api
from app.category.routes import category_api
from app.order.routes import order_api
from app.permission.routes import permission_api
from app.product.routes import product_api
from app.role.routes import role_api
from app.status.routes import status_api
from app.user.routes import user_api
app.register_blueprint(auth_api)
app.register_blueprint(category_api)
app.register_blueprint(order_api)
app.register_blueprint(permission_api)
app.register_blueprint(product_api)
app.register_blueprint(role_api)
app.register_blueprint(status_api)
app.register_blueprint(user_api)

# Setup SMTPHandler for email AUTH
mail_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),
    fromaddr=os.environ.get('APP_EMAIL'),
    toaddrs=os.environ.get('ADMIN_EMAIL'),
    subject='FlASK SHOP API ERROR',
    credentials=(os.environ.get('APP_EMAIL'), os.environ.get('APP_EMAIL_PASSWORD')),
    secure=''

)
# Set the mail handler to log ERROR
mail_handler.setLevel(logging.ERROR)
# Set format for email
mail_handler.setFormatter(logging.Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''
))

# log to email when app is not in debug mode
if not app.debug:
    app.logger.addHandler(mail_handler)

if __name__ == "__main__":
    app.run()
