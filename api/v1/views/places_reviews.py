#!/usr/bin/python3
"""
    URI file for all cities related requests
                                                """
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def hbnb_reviews(place_id):
    """
        Retrieves the list of all Review objects
                                                """
    reviews_objects = storage.get(Place, place_id)

    if not reviews_objects:
        abort(404)

    reviews = [review.to_dict() for review in storage.all(Review).values()]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def hbnb_review_id(review_id):
    """
        Returns review obj with the provided ID
                                                """
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def hbnb_review_delete(review_id):
    """
        Deletes review obj based on ID provided
                                                """
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def hbnb_review_post(place_id):
    """
        Creates a Review obj with the POST request data
                                                        """
    place_objects = storage.get(Place, place_id)

    if not place_objects:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    review_data = request.get_json()

    if not review_data.get('user_id'):
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    users_objects = storage.get(User, review_data.get('user_id'))

    if not users_objects:
        abort(404)

    if not review_data.get('text'):
        return make_response(jsonify({'error': 'Missing text'}), 400)

    new_obj = Review(**review_data)

    storage.new(new_obj)
    storage.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def hbnb_review_put(review_id):
    """
        Updates a review with specified ID if it exists
                                                                    """
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    review_data = request.get_json()

    for key, value in review_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'place_id', 'user_id']:
            setattr(review_obj, key, value)

    storage.save()

    return make_response(jsonify(review_obj.to_dict()), 200)
