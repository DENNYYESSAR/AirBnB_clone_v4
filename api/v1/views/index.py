##!/usr/bin/python3
""" Index view for the API v1 """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Returns the number of each object type """
    classes = {
        'User': storage.count('User'),
        'State': storage.count('State'),
        'City': storage.count('City'),
        'Amenity': storage.count('Amenity'),
        'Place': storage.count('Place'),
        'Review': storage.count('Review')
    }
    return jsonify(classes)


