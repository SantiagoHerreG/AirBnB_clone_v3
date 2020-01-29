#!/usr/bin/python3
""" New module for a view to Users objects
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from models import storage
from models.user import User
from flask import request


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def new_user():
    """Creates a User
    """
    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "email" not in new_obj.keys():
        abort(400, "Missing email")
    if "password" not in new_obj.keys():
        abort(400, "Missing password")

    new_user = User(**new_obj)
    new_user.save()
    storage.reload()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    for key, value in new_obj.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    storage.reload()
    return jsonify(user.to_dict()), 200


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """Retrieves list of all User
    """
    list_res = []

    users = storage.all(User)
    for user in users.values():
        list_res.append(user.to_dict())
    return jsonify(list_res)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user by its id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """Retrieves a User object by its id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())
