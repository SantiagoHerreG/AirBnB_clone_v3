#!/usr/bin/python3
""" New module for a view to City objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.state import State
from flask import request
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def new_city(state_id):
    """Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "name" not in new_obj.keys():
        abort(400, "Missing name")

    new_obj["state_id"] = state_id
    new_city = City(**new_obj)
    new_city.save()
    storage.reload()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    updated_city = city.to_dict()
    for key, value in new_obj.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            updated_city[key] = value

    city.delete()
    new_city = City(**updated_city)
    new_city.save()
    storage.reload()
    return jsonify(new_city.to_dict()), 200


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_of_state(state_id):
    """Retrieves list of all cities in a state
    """
    list_res = []

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    for city in cities.values():
        if city.state_id == state.id:
            list_res.append(city.to_dict())
    return jsonify(list_res)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city by its id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a City object by its id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())
