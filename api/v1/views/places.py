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
from models.state import State
from flask import request


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """List Place objects depending on a Json request
    """
    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    city_list = []
    if "cities" in new_obj.keys():
        city_list = new_obj["cities"]

    if "states" in new_obj.keys():
        states_list = new_obj["states"]
        for id in states_list:
            state = storage.get(State, id)
            if state is None:
                pass
            for city in state.cities:
                if city.id not in city_list:
                    city_list.append(city.id)

    amenities_list = []
    if "amenities" in new_obj.keys():
        amenities_list = new_obj["amenities"]

    list_res = []

    if len(city_list):
        for city_id in city_list:
            city = storage.get(City, city_id)
            if city is None:
                continue
            places = city.places
            for place in places:
                ame_in_place = []
                for ame in place.amenities:
                    ame_in_place.append(ame.id)
                del place.amenities
                list_res.append(place.to_dict())
                for amenity_id in amenities_list:
                    if amenity_id not in ame_in_place:
                        list_res.remove(place.to_dict())
        return jsonify(list_res)

    if len(new_obj) == 0 or len(city_list) == 0:
        all_places = storage.all(Place)
        for place in all_places.values():
            ame_in_place = []
            for ame in place.amenities:
                ame_in_place.append(ame.id)
            del place.amenities
            list_res.append(place.to_dict())
            for amenity_id in amenities_list:
                if amenity_id not in ame_in_place:
                    list_res.remove(place.to_dict())
        return jsonify(list_res)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def new_place(city_id):
    """Creates a Place
    """
    if storage.get(City, city_id) is None:
        abort(404)

    new_obj = request.get_json()
    if new_obj is None:
        abort(400, "Not a JSON")

    if "user_id" not in new_obj.keys():
        abort(400, "Missing user_id")

    if storage.get(User, new_obj["user_id"]) is None:
        abort(404)

    if "name" not in new_obj.keys():
        abort(400, "Missing name")

    new_obj["city_id"] = city_id
    new_place = Place(**new_obj)
    new_place.save()
    storage.reload()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
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
