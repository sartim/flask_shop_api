from app import app


class TestRootApi():
    def test_root_api(self):
        client = app.test_client()
        r = client.get('/')
        assert r.status_code == 200
        assert r.data == b"Welcome!"
