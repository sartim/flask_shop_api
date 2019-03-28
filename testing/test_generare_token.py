from app import app
from testing.base import Base


class TestGenerateTokenApi(Base):
    def test_generate_token_api(self):
        client = app.test_client()
        r = client.post('/account/generate/jwt/', json=dict(email='test@mail.com', password='letmein'))
        assert r.status_code == 200
        assert 'access_token' in r.json