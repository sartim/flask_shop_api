import logging
import os
import sys

from app.core.app import app, socketio

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
    socketio.run(app, host='0.0.0.0', port=8000)
