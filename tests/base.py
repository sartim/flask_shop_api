import os

from unittest import mock
from flask_migrate import Migrate, upgrade
from sqlalchemy import text

from app.core.app import app, db
from manage import (
    add_roles, add_users, add_product_data, create_superuser_role_permissions,
    create_service_permissions_on_redis, create_service_permissions_to_db)
from app.role.models import Role
from app.user.models import UserRole
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
            create_service_permissions_on_redis()
            create_service_permissions_to_db()
            create_superuser_role_permissions()
            # Generate token for authentication header
            req = cls.client.post(
                "/api/v1/auth/generate-jwt",
                json=dict(email="admin@mail.com", password="admin_pass")
            )
            cls.headers = {
                "Authorization": "Bearer {}".format(req.json["access_token"])
            }
            cls.user_id = req.json["user"]["id"]
            role = Role.get_by_name('SUPERUSER')
            user_role = UserRole(user_id=cls.user_id, role_id=role.id)
            db.session.add(user_role)
            db.session.commit()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all()
