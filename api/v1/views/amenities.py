#!/usr/bin/python3
""" New module for a view to Amenities objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.state import State
from flask import request
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def new_amenity():
    """Creates an Amenity
    """
    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "name" not in new_obj.keys():
        abort(400, "Missing name")

    new_amenity = Amenity(**new_obj)
    new_amenity.save()
    storage.reload()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    for key, value in new_obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    storage.reload()
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Retrieves list of all Amenities
    """
    list_res = []

    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        list_res.append(amenity.to_dict())
    return jsonify(list_res)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity by its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieves an amenity object by its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())
