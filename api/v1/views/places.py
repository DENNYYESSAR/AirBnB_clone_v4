#!/usr/bin/python3
""" Place objects view for API v1 """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """ Retrieves all Place objects based on JSON request body """
    request_data = request.get_json()
    
    if request_data is None:
        abort(400, 'Not a JSON')
    
    states_ids = request_data.get('states', [])
    cities_ids = request_data.get('cities', [])
    amenities_ids = request_data.get('amenities', [])
    
    places = []
    
    if not states_ids and not cities_ids:
        places = storage.all(Place).values()
    else:
        # Get places based on states and cities
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city.id not in cities_ids:
                        places.extend(city.places)
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)
    
    # Filter places based on amenities
    if amenities_ids:
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in amenities_ids]
        places = [place for place in places if all(amenity in place.amenities for amenity in amenities)]
    
    return jsonify([place.to_dict() for place in places])
