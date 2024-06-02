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
- Routes:
  /1-hbnb: display a HTML page like 1-hbnb.html
- You must use the option strict_slashes=False in your route definition
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
import uuid

app = Flask(__name__)


@app.route('/1-hbnb/', strict_slashes=False)
def hbnb():
    """
    Route handler for '/1-hbnb/':
    - Fetches State, Amenity, and Place objects from storage
    - Sorts them by name
    - Renders '1-hbnb.html' template with the fetched objects and cache_id
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda place: place.name)

    # Generate cache ID
    cache_id = str(uuid.uuid4())

    return render_template('1-hbnb.html', states=states,
                           amenities=amenities,
                           places=places,
                           cache_id=cache_id)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Method to handle @app.teardown_appcontext:
    - Closes the storage after each request
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
