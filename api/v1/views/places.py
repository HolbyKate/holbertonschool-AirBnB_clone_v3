#!/usr/bin/python3
"""Module for handling Place objects in the RESTful API."""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def get_places():
    """Retrieves the list of all Place objects"""
    places = storage.all(Place).values()
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")
    if storage.get(User, body["user_id"]) is None:
        abort(404)
    if "name" not in body:
        abort(400, "Missing name")
    body["city_id"] = city_id
    place = Place(**body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """Creates a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ["id", "user_id", "city_id", "created_at",
                       "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


if __name__ == "__main__":
    pass
