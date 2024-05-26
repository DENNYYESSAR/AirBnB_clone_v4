#!/usr/bin/python3
""" Flask application setup """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close storage session """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
