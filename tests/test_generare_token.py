from tests.base import Base


class TestGenerateTokenApi(Base):
    def test_generate_token_api(self):
        req = self.client.post(self.generate_jwt_url,
                               json=dict(email='demo2@mail.com',
                                         password='qwertytrewq'))
        assert req.status_code == 200
        assert 'access_token' in req.json
