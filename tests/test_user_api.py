from tests.base import Base


class TestUserApi(Base):
    url = '/account/user/'

    def test_get(self):
        r = self.client.get(self.url, headers=self.headers)
        assert r.status_code == 200
        assert 'count' in r.json
        assert 'results' in r.json

    def test_post(self):
        r = self.client.post(self.url, json=dict(first_name='Test', last_name='User', email='test1@mail.com',
                                                 phone='34534535', password='test'))
        assert r.status_code == 201
        assert r.json['message'] == 'Successfully saved new user'
