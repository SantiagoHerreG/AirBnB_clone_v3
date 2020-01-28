#!/usr/bin/python3
""" New module for a view to State objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.state import State
from flask import request


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """Creates a State
    """
    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "name" not in new_obj.keys():
        abort(400, "Missing name")

    new_state = State(**new_obj)
    new_state.save()
    storage.reload()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    updated_state = state.to_dict()
    for key, value in new_obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            updated_state[key] = value

    state.delete()
    new_state = State(**updated_state)
    new_state.save()
    storage.reload()
    return jsonify(new_state.to_dict()), 200


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """Retrieves list of all states
    """
    list_res = []

    states = storage.all(State)
    for state in states.values():
        list_res.append(state.to_dict())
    return jsonify(list_res)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state by its id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states_by_id(state_id):
    """Retrieves a State object by its id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
