import os

from unittest import mock
from flask_migrate import Migrate, upgrade
from sqlalchemy import text

from app import app, db
from manage import add_roles, add_users, add_product_data
from app.user import routes
from app.auth import routes
from app.role import routes
from app.permission import routes


class Base:
    @classmethod
    def setup_class(cls):
        if not os.environ.get('ENV'):
            with mock.patch.dict(os.environ, {
                'ENV': 'TEST'
            }, clear=True):
                # Assert if environment is set to TEST
                assert os.environ.get("ENV") == "TEST"
        else:
            assert os.environ.get("ENV") == "TEST"
        cls.client = app.test_client()
        cls.root_url = '/'
        cls.generate_jwt_url = '/api/v1/auth/generate-jwt'
        cls.user_url = '/api/v1/users'
        cls.permission_url = '/api/v1/permissions'
        cls.role_url = '/api/v1/roles'
        cls.category_url = '/api/v1/categories'
        cls.status_url = '/api/v1/statuses'
        with app.app_context():
            Migrate(app, db)
            db.session.execute(
                text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            db.session.commit()
            upgrade()
            db.create_all()
            add_roles()
            add_users()
            add_product_data()
            # Generate token for authentication header
            req = cls.client.post(
                "/api/v1/auth/generate-jwt",
                json=dict(email="admin@mail.com", password="admin_pass")
            )
            cls.headers = {
                "Authorization": "Bearer {}".format(req.json["access_token"])
            }

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all()
