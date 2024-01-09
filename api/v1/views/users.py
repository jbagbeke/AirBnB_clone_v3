#!/usr/bin/python3
"""
    URI file for all cities related requests
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def hbnb_users():
    """
        Retrieves the list of all User objects
                                                """
    users = [user.to_dict() for user in storage.all(User).values()]

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def hbnb_user_id(user_id):
    """
        Returns user obj with the provided ID
                                                """
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_user_delete(user_id):
    """
        Deletes user obj based on ID provided
                                                """
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    storage.delete(user_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def hbnb_user_post():
    """
        Creates a User obj with the POST request data
                                                        """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    user_data = request.get_json()

    if not user_data.get('email'):
        return make_response(jsonify({'error': 'Missing email'}), 400)

    if not user_data.get('password'):
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new_obj = User(**user_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def hbnb_user_put(user_id):
    """
        Updates the values of a user with specified ID if it exists
                                                                    """
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    user_data = request.get_json()

    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)

    storage.save()

    return make_response(jsonify(user_obj.to_dict()), 200)
