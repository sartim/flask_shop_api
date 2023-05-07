import logging
import os
import sys

from app import app
# from app.core.helpers.jwt_handlers import *
from app.core.callbacks import *
from app.auth import routes
from app.user import routes
from app.role import routes
from app.permission import routes
from app.status import routes
from app.category import routes
from app.product import routes


if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s.%(funcName)s(): %(message)s - {%(pathname)s:%(lineno)d}")
    handler = logging.StreamHandler(sys.stdout)
    log_level = os.environ.get('LOG_LEVEL')
    if log_level.lower() == 'debug':
        handler.setLevel(logging.DEBUG)
    if log_level.lower() == 'info':
        handler.setLevel(logging.INFO)
    if log_level.lower() == 'warning':
        handler.setLevel(logging.WARNING)
    if log_level.lower() == 'error':
        handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.logger.info('Application Starting...')
    app.run(host='0.0.0.0', port=5000)
