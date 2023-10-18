import unittest

from tests.base import Base
from app.core.constants import Message


class TestUserApi(Base):
    def test_get_all(self):
        req = self.client.get(self.user_url, headers=self.headers)
        assert req.status_code == 200
        assert 'count' in req.json
        assert 'results' in req.json

    @unittest.skip
    def test_get_by_id(self):
        req = self.client.get(
            "{}/{}".format(self.user_url, 1),
            headers=self.headers)
        assert req.status_code == 200
        assert 'id' in req.json
        assert 'first_name' in req.json
        assert 'last_name' in req.json
        assert 'email' in req.json
        assert 'phone' in req.json
        assert 'created_at' in req.json
        assert 'updated_at' in req.json

    @unittest.skip
    def test_post(self):
        req = self.client.post(
            self.user_url,
            headers=self.headers,
            json=dict(
                first_name='Test',
                last_name='User',
                email='test1@mail.com',
                phone='34534535',
                password='test'
            )
        )
        assert req.status_code == 201
        assert req.json['message'] == 'Successfully saved new user'

    @unittest.skip
    def test_put(self):
        req = self.client.put(
            "{}/{}".format(self.user_url, self.user_id),
            headers=self.headers,
            json=dict(id=self.user_id, last_name='User2')
        )
        assert req.status_code == 201
        assert req.json['message'] == Message.SUCCESS

    @unittest.skip
    def test_delete(self):
        req = self.client.delete(
            "{}/{}".format(self.user_url, self.user_id),
            headers=self.headers,
            json=dict(id=self.user_id)
        )
        assert req.status_code == 200
        assert req.json['message'] == Message.SUCCESS
