#!/usr/bin/python3
""" New module for a view to Place amenities relationship
"""
import models
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import request


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def new_amenity_for_place(place_id, amenity_id):
    """Creates a new amenity for a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if models.storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    storage.reload()
    return jsonify(amenity.to_dict()), 201


@app_views.route("places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities_by_place(place_id):
    """Retrieves list of all amenities of a place
    """
    list_res = []

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = place.amenities
    for amenity in amenities:
        list_res.append(amenity.to_dict())
    return jsonify(list_res)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_in_place(place_id, amenity_id):
    """Deletes an amenity by place and its id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if models.storage_t != 'db':
        place.amenity_ids.remove(amenity)
    else:
        place.amenities.remove(amenity)
    storage.save()
    storage.reload()
    return jsonify({}), 200
