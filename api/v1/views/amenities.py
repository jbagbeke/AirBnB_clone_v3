#!/usr/bin/python3
"""
    URI file for all cities related requests
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def hbnb_amenities():
    """
        Retrieves the list of all Amenity objects
                                                """
    amenities = [amen.to_dict() for amen in storage.all(Amenity).values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_amenity_id(amenity_id):
    """
        Returns amenity obj with the provided ID
                                                """
    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_amenity_delete(amenity_id):
    """
        Deletes amenity obj based on ID provided
                                                """
    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def hbnb_amenity_post():
    """
        Creates an Amenity obj with the POST request data
                                                        """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    amenity_data = request.get_json()

    if not amenity_data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_obj = Amenity(**amenity_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def hbnb_amenity_put(amenity_id):
    """
        Updates the values of a state with specified ID if it exists
                                                                    """
    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    amenity_data = request.get_json()

    for key, value in amenity_data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue

        setattr(amenity_obj, key, value)

    storage.save()

    return make_response(jsonify(amenity_obj.to_dict()), 200)
