#!/usr/bin/python3
""" New module for a view to Users objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import request


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def new_place():
    """Creates a Place
    """
    if storage.get(City, city_id) is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "user_id" not in new_obj.keys():
        abort(400, "Missing name")

    if storage.get(User, new_obj["user_id"]) is None:
        abort(404)

    if "name" not in new_obj.keys():
        abort(400, "Missing name")

    new_user = User(**new_obj)
    new_user.save()
    storage.reload()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object
    """
    place = storage.get(Place, place_id)
    if user is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    for key, value in new_obj.items():
        if key not in ["id", "user_id", "city_id" "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    storage.reload()
    return jsonify(place.to_dict()), 200


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_in_city(city_id):
    """Retrieves list of all places in a city
    """
    list_res = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = city.places
    for place in places:
        list_res.append(place.to_dict())
    return jsonify(list_res)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place by its id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a Place object by its id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())
