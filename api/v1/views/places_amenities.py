#!/usr/bin/python3
"""
    A new for the link between Place objects and Amenity objects
                                                                """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, make_response, abort


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_place_amenity(place_id):
    """
        Retrieves the list of all Amenity objects of a Place
                                                            """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    place_amenities = [amenity_obj.to_dict()
                       for amenity_obj in place_obj.amenities]

    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_amenity_places(place_id, amenity_id):
    """
        Deletes a Amenity object to a Place
                                            """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    if amenity_obj not in place_obj.amenities:
        abort(404)

    place_obj.amenities.remove(amenity_obj)

    storage.delete(amenity_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['POST'])
def hbnb_places_obj(place_id, amenity_id):
    """
        Link a Amenity object to a Place
                                        """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    if amenity_obj in place_obj.amenities:
        return make_response(jsonify(amenity_obj.to_dict()), 200)

    place_obj.amenities.append(amenity_obj)

    storage.save()

    return make_response(jsonify(amenity_obj.to_dict()), 201)
