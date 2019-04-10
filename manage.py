import logging
import sys
import csv
import os
import random

from click import prompt
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, prompt_bool, Shell, prompt_pass
from app import db
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.product.models import Product
from app.product.category.models import ProductCategory
from app.order.models import Order
from app.order.status.models import OrderStatus
from app.helpers import validator, utils
from app.helpers.socket_utils import *
from app.core import models
from app.helpers.jwt_handlers import *
from app.api_imports import *
from app.product.category.models import ProductCategory
from app.product.models import Product


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


def add_demo_users():
    user = AccountUser(first_name="Demo", last_name="User", email="demo@mail.com",
                       password=utils.generate_password_hash("qwertytrewq"), is_active=True)
    db.session.add(user)
    db.session.commit()
    user_role = AccountUserRole(user_id=user.id, role_id=3)
    db.session.add(user_role)
    db.session.commit()
    user = AccountUser(first_name="Demo2", last_name="User", email="demo2@mail.com",
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
    add_demo_users()
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


@manager.command
def populate_client_data():
    pass


@manager.command
def populate_product_data():
    """"
    ['id', 'prices_amountmax', 'prices_amountmin', 'prices_availability', 'prices_condition',
    'prices_currency', 'prices_dateseen', 'prices_issale', 'prices_merchant', 'prices_shipping',
    'prices_sourceurls', 'asins', 'brand', 'categories', 'dateadded', 'dateupdated', 'ean', 'imageurls',
    'keys', 'manufacturer', 'manufacturernumber', 'name', 'primarycategories', 'sourceurls', 'upc', 'weight']
    """
    with open('datafinitielectronicsproductspricingdata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        count = 0
        for row in csv_reader:
            price = row[1]
            brand = row[12]
            image_urls = row[17]
            name = row[21]
            category = row[22]
            items = random.randint(5, 50)

            product = Product.get_or_create_by_name(name)
            product.price = price
            product.brand = brand
            product.image_urls = image_urls
            category = ProductCategory.get_or_create_by_name(category)
            product.category_id = category.id
            product.items = items
            count+=1
            if count == 2000:
                break

@manager.command
def populate_order_data():
    pass



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
