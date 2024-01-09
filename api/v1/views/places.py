#!/usr/bin/python3
"""
    URI file for all cities related requests
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_places(city_id):
    """
        Retrieves the list of all Place objects
                                                """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    places = [place.to_dict() for place in city_obj.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def hbnb_place_id(place_id):
    """
        Returns place obj with the provided ID
                                                """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_place_delete(place_id):
    """
        Deletes place obj based on ID provided
                                                """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def hbnb_place_post(city_id):
    """
        Creates a Place obj with the POST request data
                                                        """
    cities_objects = storage.get(City, city_id)
    if not cities_objects:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    place_data = request.get_json()

    if not place_data.get('user_id'):
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    users_objects = storage.get(User, place_data.get('user_id'))
    if not users_objects:
        abort(404)

    if not place_data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_obj = Place(**place_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def hbnb_place_put(place_id):
    """
        Updates a place with specified ID if it exists
                                                                    """
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    place_data = request.get_json()

    for key, value in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)

    storage.save()

    return make_response(jsonify(place_obj.to_dict()), 200)
