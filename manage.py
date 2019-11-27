import logging
import sys
import csv
import os
import random
import click

from flask import current_app
from flask.cli import FlaskGroup

from app.core.helpers.socket_utils import *
from app.core.helpers.jwt_handlers import *
from app.core.helpers import utils, validator
from app.core import models
from app.permission.models import Permission
from app.role.models import Role, RolePermission
from app.user.models import User
from app.category.models import Category
from app.product.models import Product
from app.order.models import Order, OrderStatus
from app.order.item.models import OrderItem
from app.api_imports import *


@app.shell_context_processor
def _make_context():
    return dict(app=app, db=db, models=models)


@click.group(cls=FlaskGroup, create_app=app)
def main():
    """This is a management script for the application."""


@main.command('run', short_help='Run development server.')
def runserver():
    socketio.run(app)


@main.command('shell', short_help='Run a shell in the app context.')
def shell_command():
    ctx = current_app.make_shell_context()
    try:
        from IPython import start_ipython
        start_ipython(argv=(), user_ns=ctx)
    except ImportError:
        print(ImportError)
        from code import interact
        interact(local=ctx)


def add_roles():
    objects = [
        AccountRole(name='SUPERUSER'),
        AccountRole(name='ADMIN'),
        AccountRole(name='STAFF'),
        AccountRole(name='CLIENT')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_demo_users():
    user = AccountUser(first_name="Demo", last_name="User",
                       email="demo@mail.com", phone="254712345678",
                       password=utils.generate_password_hash("qwertytrewq"),
                       is_active=True)
    db.session.add(user)
    db.session.commit()
    user_role = AccountUserRole(user_id=user.id, role_id=3)
    db.session.add(user_role)
    db.session.commit()
    user = AccountUser(first_name="Demo2", last_name="User",
                       email="demo2@mail.com", phone="254787654321",
                       password=utils.generate_password_hash("qwertytrewq"),
                       is_active=True)
    db.session.add(user)
    db.session.commit()
    user_role = AccountUserRole(user_id=user.id, role_id=3)
    db.session.add(user_role)
    db.session.commit()


def add_order_statuses():
    objects = [OrderStatus(name='DRAFT'), OrderStatus(name='PENDING'),
               OrderStatus('COMPLETE')]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_client_data():
    pass


def add_product_data():
    with open('electronic_products_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
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
            product.save()
            click.echo("Successfully finished adding data ")


@main.command('create', short_help='Creates database tables from sqlalchemy models.')
def create():
    """
    Creates database tables from sqlalchemy models
    :param default_data:
    :param sample_data:
    """
    db.create_all()
    add_roles()
    add_demo_users()
    add_order_statuses()
    add_product_data()
    click.echo("Finished creating tables!!! \n")


@main.command('drop', short_help='Drops database tables.')
def drop():
    """Drops database tables"""""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('Finished dropping tables!!!')


@main.command('recreate', short_help='Recreates database tables.')
def recreate(default_data=True, sample_data=False):
    """
    Recreates database tables (same as issuing 'drop' and then 'create')
    :param default_data:
    :param sample_data: received
    """
    drop()
    create(default_data, sample_data)


@main.command('createsuperuser', short_help='Creates the superuser.')
def create_superuser():
    """Creates the superuser"""

    first_name = click.prompt("First Name")
    last_name = click.prompt("Last Name")
    email = click.prompt("Email")
    validate_email = validator.email_validator(email)
    password = click.prompt("Password", type=str)
    confirm_password = click.prompt("Confirm Password", type=str)
    validate_pwd = validator.password_validator(password)

    if not validate_email:
        click.echo("Not a valid email \n")

    if validate_pwd:
        click.echo("Not a valid password \n")

    if not validate_pwd:
        if not validate_pwd == confirm_password:
            click.echo("Passwords do not match \n")

    if validate_email and not validate_pwd:
        try:
            password = utils.generate_password_hash(password)
            user = AccountUser(first_name=first_name, last_name=last_name,
                               email=email, password=password,
                               is_active=True)
            db.session.add(user)
            db.session.commit()
            user_role = AccountUserRole(user_id=user.id, role_id=1)
            db.session.add(user_role)
            db.session.commit()
            click.echo("Successfully created admin account \n")
        except Exception as e:
            click.echo(str(e))


@main.command('createproducts', short_help='Creates products seeding data.')
def create_product_data():
    add_product_data()
    print("Finished seeding product data")


@main.command('createorders', short_help='Creates orders seeding data.')
def create_order_data():
    pass


cli = click.CommandCollection(sources=[main])

if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s.%(funcName)s(): "
        "%(message)s - {%(pathname)s:%(lineno)d}")
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
    cli()
