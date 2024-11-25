import googlemaps
import pandas as pd
import time
import openpyxl
from geopy.distance import geodesic



def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0

API_KEY = open("API_KEY.txt", "r").read()


map_client = googlemaps.Client(API_KEY)

location = (40.736211994701975, -73.9909710776519)
search_string = "coffee"
distance = miles_to_meters(1)
business_list = []

response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name="coffee shop",
        radius=distance
    )

business_list.extend(response.get("results"))
next_page_token = response.get("next_page_token")

while next_page_token:
    time.sleep(2)
    response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name="coffee shop",
        radius=distance,
        page_token=next_page_token
    )
    business_list.extend(response.get("results"))
    next_page_token = response.get("next_page_token")

df = pd.DataFrame(business_list)
df["url"] = "https://google.com/maps/place/?q=place_id:" + df["place_id"]
#  place_id is the unique id that is assigned to each business
df.to_excel("coffee_shop_list.xlsx", index=False)


