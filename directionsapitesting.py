import googlemaps
import os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from pprint import pprint


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


api_key = os.getenv('GOOGLE_API_KEY')

gmaps = googlemaps.Client(key=api_key)

# Geocoding an address
# geocode_result_start = gmaps.geocode('Hanau Händelstraße 10, Deutschland')
# geocode_result_destination = gmaps.geocode('Hanau Freiheitsplatz, Deutschland')

# pprint(geocode_result_start)
# pprint(f"Destination: {geocode_result_destination}")
# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions('Händelstraße 10, Hanau 63452, Deutschland',
                                     'Schlossplatz Hanau, Deutschland',
                                     mode="driving",
)

pprint(directions_result)