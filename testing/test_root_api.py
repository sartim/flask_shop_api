from app import app


def test_root_api():
    client = app.test_client()
    r = client.get('/')
    assert r.status_code, 200
    assert r.data, b"Welcome!"
