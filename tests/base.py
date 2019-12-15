import os

from unittest import mock
from flask_migrate import Migrate, upgrade
from app import app, db
from app.user import urls
from app.auth import urls
from app.role import urls
from app.permission import urls
from manage import add_roles, add_demo_users, add_product_data


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
        cls.generate_jwt_url = '/auth/generate-jwt'
        cls.user_url = '/users'
        cls.permission_url = '/permissions'
        cls.role_url = '/roles'
        cls.category_url = '/categories'
        cls.status_url = '/statuses'
        with app.app_context():
            Migrate(app, db)
            upgrade()
            db.create_all()
            add_roles()
            add_demo_users()
            add_product_data()
            # Generate token for authentication header
            req = cls.client.post(
                "/account/generate/jwt/", 
                json=dict(email="demo@mail.com", password="qwertytrewq")
            )
            cls.headers = {
                "Authorization": "Bearer {}".format(req.json["access_token"])
            }

    @classmethod
    def teardown_class(cls):
        db.drop_all()
