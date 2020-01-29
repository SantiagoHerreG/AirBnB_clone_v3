#!/usr/bin/python3
""" New module for a view to Reviews objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import request


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def new_review(place_id):
    """Creates a Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "user_id" not in new_obj.keys():
        abort(400, "Missing user_id")

    if storage.get(User, new_obj["user_id"]) is None:
        abort(404)

    if "text" not in new_obj.keys():
        abort(400, "Missing text")

    new_review = Review(**new_obj)
    new_review.save()
    storage.reload()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    for key, value in new_obj.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)

    review.save()
    storage.reload()
    return jsonify(review.to_dict()), 200


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """Retrieves list of all reviews of a place
    """
    list_res = []

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    for review in reviews:
        list_res.append(review.to_dict())
    return jsonify(list_res)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """Retrieves a Review object by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())
