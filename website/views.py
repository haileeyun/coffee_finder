import pandas as pd
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import googlemaps
from geopy.distance import geodesic
import json

from website import create_app
from .utils import create_coffee_shop_list

views = Blueprint('views', __name__)

def miles_to_meters(miles):
    try:
        return miles * 1609.344  # Convert miles to meters
    except:
        return 0


# Helper function to fetch coffee shop list for a given location
def fetch_coffee_shop_list(location):
    df = create_coffee_shop_list(location)
    df["distance"] = df.apply(
        lambda row: geodesic(
            (row["geometry"]["location"]["lat"], row["geometry"]["location"]["lng"]),
            location
        ).meters,
        axis=1
    )
    df = df.sort_values(by='distance')

    top_twenty = df.head(20)
    coffee_shop_names = top_twenty['name'].tolist()
    return coffee_shop_names


@views.route('/')
def home():
    location = (40.7484, 73.9857)  # Default location
    df = create_coffee_shop_list(location)

    if request.method == 'POST':
        address = request.form['address']
        geocoder = googlemaps.Geocoder()

        # Geocode the address to get the latitude and longitude
        response = geocoder.geocode(address)
        if response and response[0].get('geometry'):
            latitude = response[0]['geometry']['location']['lat']
            longitude = response[0]['geometry']['location']['lng']

            location = (latitude, longitude)
            df = create_coffee_shop_list(location)

    # Fetch the coffee shop list based on the location
    df["geometry"] = df["geometry"].apply(json.loads)
    df["distance"] = df.apply(
        lambda row: geodesic(
            (row["geometry"]["location"]["lat"], row["geometry"]["location"]["lng"]),
            location
        ).meters,
        axis=1
    )
    df = df.sort_values(by='distance')  # sort the coffee shops by distance

    top_twenty = df.head(20)  # top 10 closest coffee shops

    coffee_shop_names = top_twenty['name'].tolist()  # extract the coffee shop names

    # Pass the coffee shop names to the template
    context = {
        'coffee_shop_names': coffee_shop_names
    }

    return render_template('home.html', **context)


@views.route('/update-location', methods=['POST'])
def update_location():
    if request.method == 'POST':
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        print(f"Latitude: {latitude}, Longitude: {longitude}")

        # Update the coffee shop list based on the new location
        location = (latitude, longitude)
        df = create_coffee_shop_list(location)

        # Fetch the coffee shop list based on the new location
        df["geometry"] = df["geometry"].apply(json.loads)
        df["distance"] = df.apply(
            lambda row: geodesic(
                (row["geometry"]["location"]["lat"], row["geometry"]["location"]["lng"]),
                location
            ).meters,
            axis=1
        )
        df = df.sort_values(by='distance')  # sort the coffee shops by distance

        top_ten = df.head(10)  # top 10 closest coffee shops

        coffee_shop_names = top_ten['name'].tolist()  # extract the coffee shop names

        # Pass the coffee shop names to the template
        context = {
            'coffee_shop_names': coffee_shop_names
        }

        return jsonify(context)

    return jsonify({'message': 'Invalid request'})



