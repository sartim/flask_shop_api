from flask_cors import cross_origin
from app.core.app import app


@app.route('/')
@cross_origin()
def root():
    return "Welcome!"
