from tests.base import Base


class TestProductCategoryApi(Base):
    def test_get_all(self):
        req = self.client.get(self.product_category_url,
                              headers=self.headers)
        assert req.status_code == 200
        assert 'count' in req.json
        assert 'results' in req.json

    def test_get_by_id(self):
        req = self.client.get('{}?id=1'
                              .format(self.product_category_url),
                              headers=self.headers)
        assert req.status_code == 200
        assert 'Electronics' == req.json['name']
        assert 'name' in req.json
        assert 'created_date' in req.json
        assert 'updated_date' in req.json
