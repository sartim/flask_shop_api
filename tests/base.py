import os

from flask_migrate import Migrate, upgrade
from app import app, db
from manage import add_roles, add_demo_users, add_product_data


class Base:
    @classmethod
    def setup_class(cls):
        assert os.environ.get("TEST") == "TRUE"
        cls.client = app.test_client()
        cls.root_url = '/'
        cls.generate_jwt_url = '/account/generate/jwt/'
        cls.user_url = '/account/user/'
        cls.product_category_url = '/product/category/'
        with app.app_context():
            Migrate(app, db)
            upgrade()
            db.create_all()
            # Add pre-loaded data
            add_roles()
            add_demo_users()
            add_product_data()
            # Generate token for authentication header
            req = cls.client.post('/account/generate/jwt/', json=dict(email='demo@mail.com', password='qwertytrewq'))
            cls.headers = {'Authorization': 'Bearer {}'.format(req.json['access_token'])}

    @classmethod
    def teardown_class(cls):
        db.drop_all()
