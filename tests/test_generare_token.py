from tests.base import Base


class TestGenerateTokenApi(Base):
    def test_generate_token_api(self):
        r = self.client.post('/account/generate/jwt/', json=dict(email='demo2@mail.com', password='qwertytrewq'))
        assert r.status_code == 200
        assert 'access_token' in r.json