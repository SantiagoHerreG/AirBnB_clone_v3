#!/usr/bin/python3
""" API for the Airbnb Clone
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import make_response
from flask import jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_method(var):
    """ calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":

    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = "0.0.0.0"

    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = "5000"

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
