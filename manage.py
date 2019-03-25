import logging
import sys
import uuid
import os

from click import prompt
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, prompt_bool, Shell, prompt_pass
from app import db
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.helpers import validator, utils
from app.helpers.socket_utils import *
from app.core import models
from app.api_imports import *


def _make_context():
    return dict(app=app, db=db, models=models)


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def runserver():
    socketio.run(app, host='0.0.0.0', port=5000)


def add_roles():
    objects = [
        AccountRole(name='SUPERUSER'), AccountRole(name='ADMIN'), AccountRole(name='STAFF'),
        AccountRole(name='CLIENT')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_countries():
    # TODO Add all countries from script
    objects = [
        Country(name='UK'), Country(name='US'), Country(name='RUSSIA'),
        Country(name='CHINA')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_demo_user():
    user = AccountUser(first_name="Demo", last_name="User", email="demo@mail.com",
                       password=utils.generate_password_hash("qwertytrewq"), is_active=True)
    db.session.add(user)
    db.session.commit()
    user_role = AccountUserRole(user_id=user.id, role_id=3)
    db.session.add(user_role)
    db.session.commit()


@manager.command
def create(default_data=True, sample_data=False):
    """
    Creates database tables from sqlalchemy models
    :param default_data:
    :param sample_data:
    """
    db.create_all()
    add_roles()
    add_demo_user()
    sys.stdout.write("Finished creating tables!!! \n")


# DO NOT ever run this on production server
@manager.command
def drop():
    """Drops database tables"""""
    if prompt_bool("Are you sure you want to drop all tables?"):
        db.drop_all()
        sys.stdout.write("Finished dropping tables!!! \n")


# DO NOT ever run this on production server
# Also never run it twice
@manager.command
def recreate(default_data=True, sample_data=False):
    """
    Recreates database tables (same as issuing 'drop' and then 'create')
    :param default_data:
    :param sample_data: received
    """
    drop()
    create(default_data, sample_data)


@manager.command
def createsuperuser():
    """Creates the superuser"""

    first_name = prompt("First Name")
    last_name = prompt("Last Name")
    email = prompt("Email")
    validate_email = validator.email_validator(email)
    password = prompt_pass("Password")
    confirm_password = prompt_pass("Confirm Password")
    validate_pwd = validator.password_validator(password)

    if not validate_email:
        sys.stdout.write("Not a valid email \n")

    if validate_pwd:
        sys.stdout.write("Not a valid password \n")

    if not validate_pwd:
        if not validate_pwd == confirm_password:
            sys.stdout.write("Passwords do not match \n")

    if validate_email and not validate_pwd:
        try:
            password = utils.generate_password_hash(password)
            user = AccountUser(first_name=first_name, last_name=last_name, email=email, password=password,
                               is_active=True)
            db.session.add(user)
            db.session.commit()
            user_role = AccountUserRole(user_id=user.id, role_id=1)
            db.session.add(user_role)
            db.session.commit()
            sys.stdout.write("Successfully created admin account \n")
        except Exception as e:
            sys.stdout.write(str(e))


if __name__ == '__main__':
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
    manager.run()
