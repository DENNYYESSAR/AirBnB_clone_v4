#!/usr/bin/python3
""" Flask application setup """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close storage session """
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """ Handle 404 errors with JSON response """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
