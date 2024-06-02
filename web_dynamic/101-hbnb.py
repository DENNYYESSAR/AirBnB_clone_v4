#!/usr/bin/python3
"""
A script that starts a Flask web application:
- Your web application must be listening on 0.0.0.0, port 5000
- You must use storage for fetching data from the storage engine
(FileStorage or DBStorage)
- To load all cities of a State, if your storage engine is DBStorage,
you must use cities relationship
  Otherwise, use the public getter method cities
- After each request you must remove the current SQLAlchemy Session:
  Declare a method to handle @app.teardown_appcontext
  Call in this method storage.close()
"""
from flask import Flask, render_template, request, jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
import uuid

app = Flask(__name__)


@app.route('/101-hbnb/', strict_slashes=False)
def hbnb():
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    cities = storage.all(City).values()
    cities = sorted(cities, key=lambda city: city.name)

    return render_template('101-hbnb.html', states=states,
                           amenities=amenities,
                           cities=cities,
                           cache_id=str(uuid.uuid4()))


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
