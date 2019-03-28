import os

from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


class BaseConfig(object):
    """
    Callable Base Config which takes an object
    """
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SQLALCHEMY_DATABASE_URI = '{}'. \
        format(os.environ.get('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """
    Development config which inherits from BaseConfig
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 10


class ProductionConfig(BaseConfig):
    """
    Production config which inherits from BaseConfig
    """
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 14


class TestingConfig(BaseConfig):
    """
    Testing config which inherits from BaseConfig
    """
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 1
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.BASE_DIR, 'test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

