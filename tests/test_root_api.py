from tests.base import Base


class TestRootApi(Base):
    def test_root_api(self):
        req = self.client.get(self.root_api_url)
        assert req.status_code == 200
        assert req.data == b"Welcome!"
