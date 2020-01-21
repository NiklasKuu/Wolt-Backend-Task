import json
import queue
import haversine
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

@app.route('/restaurants/search', methods=['GET'])
def restaurant_search():
    """Returns a list of restaurants whose name, description and/or tags match the query_string
     and are closer than 3km from the paramter latitude and longitude coordinates."""
    # Get query string parameters
    query_string = request.args.get('q')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    # Check that request parameters are valid, if not send 400 response 
    if query_string == None or len(query_string) < 1:
        response_data = {
            "error": "Query string length is missing or is too short (minimum length is 1 character)"
        }
        return make_response(jsonify(response_data), 400)
    if latitude == None or not isfloat(latitude) or latitude == "":
        response_data = {
            "error": "Latitude coordinate is missing or is not a float."
        }
        return make_response(jsonify(response_data), 400)
    if longitude == None or not isfloat(longitude) or longitude == "":
        response_data = {
            "error": "Longitude coordinate is missing is not a float."
        }
        return make_response(jsonify(response_data), 400)

    try:
        # load json file into dict
        json_file = open("restaurants.json", "r")
        json_data = json.load(json_file)


        matching_restaurants = []
        for restaurant in json_data["restaurants"]:
            # Get restaurant name, description, and tags and concatenate into one string
            concatenation = restaurant["name"] + restaurant["description"]
            for tag in restaurant["tags"]:
                concatenation += tag
            # Filter restaurants in lowercase while removing all whitespaces from concatenation and query string string, such as space, tab, newline, etc.
            if "".join(query_string.split()).lower() in "".join(concatenation.split()).lower():
                # If filter matches, calculate distance using haversine formula assuming location in json data is stored in format [lon, lat].
                distance = haversine.haversine((float(latitude), float(
                    longitude)), (restaurant["location"][1], restaurant["location"][0]))
                if distance < 3:
                    matching_restaurants.append(restaurant)
        return make_response(jsonify(matching_restaurants), 200)
    except Exception as exc:
        print(exc)
        response_data = {
            "error": "Unexpected Server error."
        }
        return make_response(jsonify(response_data), 500)


def isfloat(value):
    """Returns True if value can be converted to float, otherwise returns False.\n
    :param value: The value to be checked.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run()
