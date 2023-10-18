import unittest

from app import app
from app.core.helpers import utils
from app.core.constants import ResponseMessage
from manage import add_order_statuses
from app.status.models import Status
from tests.base import Base


class TestStatusApi(Base):
    def test_get_all(self):
        self.headers["Content-type"] = "application/json"
        req = self.client.get(self.status_url, headers=self.headers)
        assert req.status_code == 200
        assert "results" in req.json

    @unittest.skip
    def test_get_by_id(self):
        with app.app_context():
            add_order_statuses()
            self.headers["Content-type"] = "application/json"
            status = Status.get_by_name('PENDING')
            if status:
                req = self.client.get("{}/{}".format(
                    self.status_url, status.id), headers=self.headers
                )
                assert req.status_code == 200
                assert "name" in req.json
                assert "description" in req.json
            else:
                raise ValueError("Test Failed")

    @unittest.skip
    def test_post(self):
        data = utils.open_file("data/statuses.json")
        self.headers["Content-type"] = "application/json"
        for item in data:
            req = self.client.post(
                self.status_url,
                headers=self.headers,
                json=item
            )
            assert req.status_code == 201
            assert "message" in req.json
            assert ResponseMessage.RECORD_SAVED == req.json["message"]

    @unittest.skip
    def test_put(self):
        with app.app_context():
            self.headers["Content-type"] = "application/json"
            payload = dict(description="Bank loan")
            status = Status.get_by_name('PENDING')
            req = self.client.put(
                "{}/{}".format(self.status_url, status.id), headers=self.headers,
                json=payload
            )
            assert req.status_code == 200
            assert req.json["message"] == ResponseMessage.RECORD_UPDATED

    @unittest.skip
    def test_delete(self):
        with app.app_context():
            self.headers["Content-type"] = "application/json"
            status = Status.get_by_name('PENDING')
            req = self.client.delete(
                "{}/{}".format(self.status_url, status.id), headers=self.headers
            )
            assert req.status_code == 204
