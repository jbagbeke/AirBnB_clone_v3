#!/usr/bin/python3
"""
    Entry point of the API if I'm right
                                        """
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.city import City


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """
        Returns a jsonified reply og the stat of the api
                                                        """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def hbnb_count():
    """
        Returns number of counts by class
                                        """
    cls_stats = {
               'amenities': storage.count(Amenity),
               'cities': storage.count(City),
               'places': storage.count(Place),
               'reviews': storage.count(Review),
               'states': storage.count(State),
               'users': storage.count(User)
               }
    return jsonify(cls_stats)
