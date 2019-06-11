from flask_migrate import Migrate, upgrade
from app import app, db
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.product.models import Product
from app.product.category.models import ProductCategory
from app.order.models import Order
from app.order.status.models import OrderStatus
from app.helpers import utils
from app.api_imports import *
from manage import add_roles, add_demo_users


class Base:
    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()
        cls.root_api_url = '/'
        cls.generate_jwt_api_url = '/account/generate/jwt/'
        cls.user_api_url = '/account/user/'
        with app.app_context():
            Migrate(app, db)
            upgrade()
            db.create_all()
            # Add pre-loaded data
            add_roles()
            add_demo_users()
            # Generate token for authentication header
            r = cls.client.post('/account/generate/jwt/', json=dict(email='demo@mail.com', password='qwertytrewq'))
            cls.headers = {'Authorization': 'Bearer {}'.format(r.json['access_token'])}

    @classmethod
    def teardown_class(cls):
        db.drop_all()
        db.engine.execute("DROP TABLE alembic_version")
