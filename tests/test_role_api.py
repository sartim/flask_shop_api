import unittest

from app.core.helpers import utils
from app.core.constants import ResponseMessage
from tests.base import Base


class TestRoleApi(Base):
    @unittest.skip
    def test_get_all(self):
        self.headers["Content-type"] = "application/json"
        req = self.client.get(self.role_url, headers=self.headers)
        assert req.status_code == 200
        assert "results" in req.json

    @unittest.skip
    def test_get_by_id(self):
        self.headers["Content-type"] = "application/json"
        req = self.client.get("{}/{}".format(
            self.role_url, 1), headers=self.headers
        )
        assert req.status_code == 200
        assert "name" in req.json
        assert "permissions" in req.json

    @unittest.skip
    def test_post(self):
        data = utils.open_file("data/roles.json")
        self.headers["Content-type"] = "application/json"
        for item in data:
            req = self.client.post(
                self.role_url,
                headers=self.headers,
                json=item
            )
            assert req.status_code == 201
            assert "message" in req.json
            assert ResponseMessage.RECORD_SAVED == req.json["message"]

    @unittest.skip
    def test_put(self):
        self.headers["Content-type"] = "application/json"
        payload = dict(description="Role description")
        req = self.client.put(
            "{}/{}".format(self.role_url, 1), headers=self.headers,
            json=payload
        )
        assert req.status_code == 200
        assert req.json["message"] == ResponseMessage.RECORD_UPDATED

    @unittest.skip
    def test_delete(self):
        self.headers["Content-type"] = "application/json"
        req = self.client.delete(
            "{}/{}".format(self.role_url, 1), headers=self.headers
        )
        assert req.status_code == 204
