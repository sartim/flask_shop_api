from testing.base import Base


class TestUserApi(Base):
    def test_get(self):
        r = self.client.get('/account/user/', headers=self.headers)
        assert r.status_code == 200
        assert 'count' in r.json
        assert 'results' in r.json
