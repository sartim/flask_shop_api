import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    """
    Callable Base Config which takes an object
    """
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')
    )
    SQLALCHEMY_DATABASE_URI = '{}'. \
        format(os.environ.get('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REDIS_URL = os.environ.get('REDIS_URL')
    CACHED_QUERY = os.environ.get("CACHED_QUERY")
    REDIS_EXPIRE = os.environ.get('REDIS_EXPIRE')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 3700
    JWT_ERROR_MESSAGE_KEY = "message"
    PAGINATE_BY = os.environ.get("PAGINATE_BY")
    LOG_LEVEL = os.environ.get("LOG_LEVEL")


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
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

