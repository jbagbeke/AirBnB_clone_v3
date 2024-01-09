#!/usr/bin/python3
"""
    URI file for all cities related requests
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_cities(state_id):
    """
        Retrieves the list of all City objects
                                                """
    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    cities = [city.to_dict() for city in storage.all(City).values()]

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def hbnb_city_id(city_id):
    """
        Returns city obj with the provided ID
                                                """
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_city_delete(city_id):
    """
        Deletes city obj based on ID provided
                                                """
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    storage.delete(city_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def hbnb_city_post(state_id):
    """
        Creates a City obj with the POST request data
                                                    """
    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    city_data = request.get_json()

    if not city_data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_obj = City(state_id=state_obj.id, **city_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def hbnb_city_put(city_id):
    """
        Updates the values of a city with specified ID if it exists
                                                                    """
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    city_data = request.get_json()

    if not city_data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    for key, value in city_data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue

        setattr(city_obj, key, value)

    storage.save()

    return make_response(jsonify(city_obj.to_dict()), 200)
