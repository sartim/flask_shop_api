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
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
from app.core.connection import elasticsearch

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


def create_app():
    app = Flask(__name__)
    if os.environ.get('DEV') == "TRUE":
        app.config.from_object(DevelopmentConfig)
        app.elasticsearch = elasticsearch
        app.logger.debug(" * ENV: DEVELOPMENT")
    if os.environ.get('PROD') == "TRUE":
        app.config.from_object(ProductionConfig)
        app.elasticsearch = elasticsearch
        app.logger.debug(" * ENV: PRODUCTION")
    if os.environ.get("TEST") == "TRUE":
        app.config.from_object(TestingConfig)
        app.elasticsearch = None
        app.logger.debug(" * ENV: TESTING")
    return app


app = create_app()

db = SQLAlchemy(app)
db.init_app(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(app, supports_credentials=True)

socketio = SocketIO(app)

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
