from tests.base import Base


class TestProductCategoryApi(Base):
    def test_get(self):
        req = self.client.get(self.product_category_url,
                              headers=self.headers)
        assert req.status_code == 200
        assert 'count' in req.json
        assert 'results' in req.json
