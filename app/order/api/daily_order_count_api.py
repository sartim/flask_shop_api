from flask import jsonify
from flask.views import MethodView
from app import app
from app.core.helpers import data_generator


class DailyOrderCount(MethodView):
    # @cross_origin()
    # @jwt_required
    def get(self):
        return jsonify(data_generator.get_date_values())


app.add_url_rule('/order/daily/count/',
                 view_func=DailyOrderCount.as_view('daily-published-count'), methods=['GET'])
