from tests.base import Base


class TestRootApi(Base):
    def test_root_api(self):
        r = self.client.get('/')
        assert r.status_code == 200
        assert r.data == b"Welcome!"
