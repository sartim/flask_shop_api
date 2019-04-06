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


class Base:
    @classmethod
    def setup_class(cls):
        with app.app_context():
            Migrate(app, db)
            upgrade()
            db.create_all()

            objects = [
                AccountRole(name='SUPERUSER'), AccountRole(name='ADMIN'), AccountRole(name='STAFF'),
                AccountRole(name='CLIENT')
            ]
            db.session.bulk_save_objects(objects)
            db.session.commit()

            user = AccountUser(first_name="Test", last_name="User", email="test@mail.com",
                               password=utils.generate_password_hash("letmein"), is_active=True)
            db.session.add(user)
            db.session.commit()
            user_role = AccountUserRole(user_id=user.id, role_id=3)
            db.session.add(user_role)
            db.session.commit()

    @classmethod
    def teardown_class(cls):
        db.drop_all()
        db.engine.execute("DROP TABLE alembic_version")
