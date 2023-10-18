import unittest

from tests.base import Base


class TestCategoryApi(Base):
    def test_get_all(self):
        req = self.client.get(
            self.category_url,
            headers=self.headers
        )
        assert req.status_code == 200
        assert 'count' in req.json
        assert 'results' in req.json

    @unittest.skip
    def test_get_by_id(self):
        req = self.client.get(
            '{}/{}'.format(self.category_url, 1),
            headers=self.headers)
        assert req.status_code == 200
        assert 'name' in req.json
        assert 'created_date' in req.json
        assert 'updated_date' in req.json
