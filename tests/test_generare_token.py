from tests.base import Base


class TestGenerateTokenApi(Base):
    def test_generate_token_api(self):
        req = self.client.post(self.generate_jwt_url,
                               json=dict(email="admin@mail.com",
                                         password="admin_pass"))
        assert req.status_code == 200
        assert 'access_token' in req.json
