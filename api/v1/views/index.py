#!/usr/bin/python3
""" New module for index.py
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place


@app_views.route("/status")
def status():
    """First route that returns the status in json format
    """
    dict_res = {"status": "OK"}
    return jsonify(dict_res)


@app_views.route("/stats")
def stats():
    """endpoint that retrieves the number of each objects by type
    """
    objs = [(Amenity, "amenities"), (City, "cities"), (Place, "places"),
            (Review, "reviews"), (State, "states"), (User, "users")]

    res_dict = {}

    for obj in objs:
        res_dict[obj[1]] = storage.count(obj[0])

    return jsonify(res_dict)
