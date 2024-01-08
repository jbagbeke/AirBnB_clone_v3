#!/usr/bin/python3
"""
    Flask App to handle state requests to the API
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def hbnb_states():
    """
        Retrieves the list of all State objects
                                                """
    all_states = [state.to_dict() for state in storage.all(State).values()]

    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def hbnb_states_id(state_id):
    """
        Returns state obj with the provided ID
                                                """
    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_states_delete(state_id):
    """
        Deletes state obj based on ID provided
                                                """
    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    storage.delete(state_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def hbnb_state_post():
    """
        Creates a State obj with the POST request data
                                                        """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    state_data = request.get_json()

    if not state_data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_obj = State(**state_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def hbnb_state_put(state_id):
    """
        Updates the values of a state with specified ID if it exists
                                                                    """
    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    state_data = request.get_json()

    for key, value in state_data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue

        setattr(state_obj, key, value)

    storage.save()

    return make_response(jsonify(state_obj.to_dict()), 200)
