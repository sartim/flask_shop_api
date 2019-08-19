import os
from flask import jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename

from app import app
from app.core.helpers.utils import allowed_file


class BaseResource(MethodView):
    @staticmethod
    def upload(folder, file):
        """Uploads to file directory. You can update to use S3 bucket or any external storage"""
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = "{}{}/{}".format(os.getcwd(), app.config['UPLOAD_FOLDER'], folder)
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except Exception as e:
                    app.logger.debug(str(e))
            try:
                file.save(os.path.join(path, filename))
                return os.path.join(folder, filename)
            except Exception as e:
                app.logger.error("Error creating directory. {}".format(str(e)))
                return None

    @staticmethod
    def response(data, status=200):
        return jsonify(data), status
