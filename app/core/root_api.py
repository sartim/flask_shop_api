from flask_cors import cross_origin
from app import app, basic_auth


@app.route('/')
@cross_origin()
@basic_auth.required
def root():
    return "Welcome!"
