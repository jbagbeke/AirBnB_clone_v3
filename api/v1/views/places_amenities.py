#!/usr/bin/python3
"""
    A new for the link between Place objects and Amenity objects
                                                                """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, make_response


@app_views.route('/api/v1/places/<place_id>/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_place_amenity(place_id):
    """
        Retrieves the list of all Amenity objects of a Place
                                                            """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)
    place_amenity_ids = place_obj.amenity_ids

    place_amenities = [storage.get(Amenity, amenity_id).to_dict()
                       for amenity_id in place_amenity_ids]

    return jsonify(place_amenities)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_amenity_delete(place_id, amenity_id):
    """
        Deletes a Amenity object to a Place
                                            """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    place_amenity_ids = place_obj.amenity_ids

    if amenity_id not in place_amenity_ids:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    return jsonify({})


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['POST'])
def hbnb_amenity_post(place_id, amenity_id):
    """
        Link a Amenity object to a Place
                                        """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    place_amenity_ids = place_obj.amenity_ids

    if amenity_id in place_amenity_ids:
        return make_response(jsonify(amenity_obj.to_dict()), 200)

    place_obj.amenity_ids = place_amenity_ids.append(amenity_id)
    place_obj.amenities = amenity_obj

    storage.save()

    return make_response(jsonify(amenity_obj.to_dict()), 201)

