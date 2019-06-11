from tests.base import Base


class TestUserApi(Base):
    def test_get(self):
        req = self.client.get(self.user_api_url, headers=self.headers)
        assert req.status_code == 200
        assert 'count' in req.json
        assert 'results' in req.json

    def test_post(self):
        req = self.client.post(self.user_api_url,
                               json=dict(first_name='Test',
                                         last_name='User',
                                         email='test1@mail.com',
                                         phone='34534535',
                                         password='test'))
        assert req.status_code == 201
        assert req.json['message'] == 'Successfully saved new user'
