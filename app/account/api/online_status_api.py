from flask import jsonify
from flask.views import MethodView
from app import app
from app.account.user.models import AccountUser


class OnlineStatus(MethodView):
    def get(self):
        data = AccountUser.get_online_users()
        if data:
            return jsonify(data)
        return jsonify({"count": 0, "results": []})

app.add_url_rule('/account/user/online/', view_func=OnlineStatus.as_view('online-status'),
                 methods=['GET'])