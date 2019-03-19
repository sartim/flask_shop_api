import logging
import sys
import uuid

from click import prompt
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, prompt_bool, Shell, prompt_pass
from app import db
# from app.article.migration import article
# from app.account.migration import account
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.account.user.message.models import AccountUserMessage
from app.article.body.models import ArticleBody
from app.article.body.type.models import ArticleBodyType
from app.article.rejection.category.models import ArticleRejectionCategory
from app.article.status.models import ArticleStatus
from app.article.version.models import ArticleVersion
from app.article.category.models import ArticleCategory
from app.article.location.models import ArticleLocation
from app.helpers import validator, utils, date_time, email
from app.helpers.socket_utils import *
from app.core import models
from app.article.materialized_view.helpers import refresh_materialized_view as rmv
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


def add_default_roles():
    objects = [
        AccountRole(name='SUPERUSER'), AccountRole(name='ADMIN'), AccountRole(name='WRITER'),
        AccountRole(name='EDITOR')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_article_status():
    objects = [
        ArticleStatus(name='draft'), ArticleStatus(name='pending'), ArticleStatus(name='review'),
        ArticleStatus(name='rejected'), ArticleStatus(name='published'), ArticleStatus(name='deleted')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_locations():
    objects = [
        ArticleLocation(name='All'), ArticleLocation(name='National'), ArticleLocation(name='Garissa'),
        ArticleLocation(name='Kiambu'), ArticleLocation(name='Nairobi'), ArticleLocation(name='Kibera'),
        ArticleLocation(name='Kisii'), ArticleLocation(name='Kisumu'), ArticleLocation(name='Machakos'),
        ArticleLocation(name='Mombasa'), ArticleLocation(name='Nakuru'), ArticleLocation(name='Nyamira'),
        ArticleLocation(name='Uasin Gishu')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_categories():
    objects = [
        ArticleCategory(name='Politics'), ArticleCategory(name='Opinion'), ArticleCategory(name='Business'),
        ArticleCategory(name='Agriculture'), ArticleCategory(name='Crime'), ArticleCategory(name='Sport'),
        ArticleCategory(name='Entertainment'), ArticleCategory(name='Event'), ArticleCategory(name='Education'),
        ArticleCategory(name='Transport'), ArticleCategory(name='Health'), ArticleCategory(name='News'),
        ArticleCategory(name='Environment'), ArticleCategory(name='Random'), ArticleCategory(name='Tubonge'),
        ArticleCategory(name='Lifestyle')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_rejection_categories():
    objects = [
        ArticleRejectionCategory(name='No local angle'), ArticleRejectionCategory(name='Too similar'),
        ArticleRejectionCategory(name='No photo caption'), ArticleRejectionCategory(name='Poor quality photo'),
        ArticleRejectionCategory(name='Time barred'), ArticleRejectionCategory(name='Plagiarism'),
        ArticleRejectionCategory(name='Not engaging'), ArticleRejectionCategory(name='Inappropriate content'),
        ArticleRejectionCategory(name='Informal writing style'), ArticleRejectionCategory(name='Too short'),
        ArticleRejectionCategory(name='Duplicate'), ArticleRejectionCategory(name='Headline not compelling'),
        ArticleRejectionCategory(name='Not educative'), ArticleRejectionCategory(name='Not verifiable'),
        ArticleRejectionCategory(name='No unique photo'), ArticleRejectionCategory(name='Information not attributed'),
        ArticleRejectionCategory(name='Other')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


@manager.command
def add_body_types():
    objects = [
        ArticleBodyType(name='TEXT'), ArticleBodyType(name='HTML'), ArticleBodyType(name='MARKDOWN')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


@manager.command
def create(default_data=True, sample_data=False):
    """
    Creates database tables from sqlalchemy models
    :param default_data:
    :param sample_data:
    """
    db.create_all()
    add_article_status()
    add_default_roles()
    add_body_types()
    add_locations()
    add_categories()
    add_rejection_categories()
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
def refresh_materialized_views():
    rmv('articles')
    rmv('article_fusions')
    sys.stdout.write("Finished refreshing all materialized views!!! \n")


@manager.command
def create_article_data():
    current_timestamp = date_time.current_timestamp()
    body = "Started migrating article index data at {}".format(current_timestamp)
    email.send(subject='ARTICLES MIGRATION START', recipients=os.environ.get('ADMIN_EMAIL'), body=body)
    print("Please wait as the article data is inserted..")
    article.article_scroll()
    print("Finished creating article data!!!")
    body = "Finished migrating article index data at {}".format(current_timestamp)
    email.send(subject='ARTICLES MIGRATION FIN', recipients=os.environ.get('ADMIN_EMAIL'), body=body)


@manager.command
def create_profile_data():
    current_timestamp = date_time.current_timestamp()
    body = "Started migrating profile index data at {}".format(current_timestamp)
    email.send(subject='PROFILE MIGRATION START', recipients=os.environ.get('ADMIN_EMAIL'), body=body)
    print("Please wait as the profile data is inserted..")
    account.get_profiles_with_scroll_api()
    print("Finished creating profile data!!!")
    body = "Finished migrating profile index data at {}".format(current_timestamp)
    email.send(subject='PROFILE MIGRATION FIN', recipients=os.environ.get('ADMIN_EMAIL'), body=body)


@manager.command
def search_reindex():
    """Re-indexes the fields for elastic search"""
    try:
        print("Please wait as the data is being indexed..")
        AccountUser.reindex()
        ArticleVersion.reindex()
        print("Finished indexing data!!!")
    except Exception as e:
        print(str(e))


@manager.command
def delete_index():
    """Deletes indices for elastic search"""
    try:
        print("Please wait as the indices are being deleted..")
        app.elasticsearch.indices.delete(AccountUser.__tablename__)
        app.elaticseach.indices.delete(ArticleVersion.__tablename__)
        print("Finished deleting indices!!!")
    except Exception as e:
        print(str(e))


@manager.command
def createsuperuser():
    """Creates the superuser"""

    full_name = prompt("Full Name")
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
            id = uuid.uuid4()
            password = utils.generate_password_hash(password)
            user = AccountUser(id=id, name=full_name, email=email, password=password)
            AccountUserRole(user_id=user.id, role_id=1)
            db.session.add(user)
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
