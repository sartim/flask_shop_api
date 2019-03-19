import os

from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


class BaseConfig(object):
    """
    Callable Base Config which takes an object
    """
    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # SQLite for this example
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = '{}'. \
        format(os.environ.get('DATABASE_URL'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')
    # Secret key
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
