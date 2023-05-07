import json
import logging
import sys
import csv
import os
import random
import click

from flask import current_app
from flask.cli import FlaskGroup
from sqlalchemy import desc
from app.core.helpers.socket_utils import *
# from app.core.helpers.jwt_handlers import *
from app.core.helpers import utils, validator
from app.core import base_model
from app.permission.models import Permission
from app.role.models import Role, RolePermission
from app.user.models import User, UserRole
from app.category.models import Category
from app.product.models import Product
from app.order.models import Order, OrderItem
from app.core.callbacks import *
from app.auth import routes
from app.user import routes
from app.role import routes
from app.permission import routes
from app.status import routes
from app.category import routes
from app.product import routes
from app.core.helpers import password_helper
from app.status.models import Status


@app.shell_context_processor
def _make_context():
    return dict(app=app, db=db, models=base_model)


@click.group(cls=FlaskGroup, create_app=app)
def main():
    """This is a management script for the application."""


@main.command('run', short_help='Run development server.')
def runserver():
    socketio.run(app, port=8000, debug=True)


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
    with open('data/roles.json') as json_file:
        items = json.load(json_file)
        objects = [Role(**item).create() for item in items]
        click.echo("Finished adding roles")
        return objects


def add_users():
    with open('data/users.json') as json_file:
        items = json.load(json_file)

        def process(item):
            roles = item['roles']
            del item['roles']
            item['password'] = password_helper.generate_password_hash(
                item['password'])
            obj, msg = User(**item).create()
            roles = [Role.get_by_name(role) for role in roles]
            obj.roles = [UserRole(obj.id, role.id) for role in roles]
            obj.save()

        objects = [process(item) for item in items]
        click.echo("Finished adding users")
        return objects


def add_order_statuses():
    with open('data/statuses.json') as json_file:
        items = json.load(json_file)
        objects = [Status(**item).create() for item in items]
        click.echo("Finished adding statuses")
        return objects


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
            category = Category.get_or_create_by_name(category)
            product.category_id = category.id
            product.items = items
            product.save()
            click.echo("Successfully finished adding data ")


@main.command('create',
              short_help='Creates database tables from sqlalchemy models.')
def create():
    """
    Creates database tables from sqlalchemy models
    :param default_data:
    :param sample_data:
    """
    db.create_all()
    def process():
        add_roles()
        add_users()
        add_order_statuses()
        # add_product_data()
        click.echo("Finished creating tables!!! \n")
    process()


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


@main.command('create-super-user', short_help='Creates the superuser.')
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
            password = password_helper.generate_password_hash(password)
            user = User(
                first_name=first_name, last_name=last_name,
                email=email, password=password,
                is_active=True)
            db.session.add(user)
            db.session.commit()
            user_role = UserRole(user_id=user.id, role_id=1)
            db.session.add(user_role)
            db.session.commit()
            click.echo("Successfully created admin account \n")
        except Exception as e:
            click.echo(str(e))


@main.command('create-products',
              short_help='Creates products seeding data.')
def create_product_data():
    add_product_data()
    print("Finished seeding product data")


@main.command('create-orders', short_help='Creates orders seeding data.')
def create_order_data():
    pass


def save_permissions(perm):
    for permission in perm["permissions"]:
        permission.update(path=perm["path"])
        p = Permission.get_by_name(permission.get("name"))
        if not p:
            last_permission_id = Permission.query.order_by(
                desc(Permission.created_at)).first().id
            _id = last_permission_id + 1
            permission.update(id=_id)
            try:
                Permission(**permission).create()
                click.echo("Created permission: {}".format(permission))
            except Exception as e:
                db.session.rollback()
                click.echo(str(e))


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
