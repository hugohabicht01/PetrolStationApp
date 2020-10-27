import os
from os.path import join, dirname

import googlemaps
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.getenv('GOOGLE_API_KEY')

gmaps = googlemaps.Client(key=api_key)

# Geocoding an address
# geocode_result_start = gmaps.geocode('Frankfurt Im Staffel 109, Deutschland')
# geocode_result_destination = gmaps.geocode('Frankfurt Hebelstraße 15, Deutschland')

# pprint(geocode_result_start[0]['geometry']['location'])
# print("-"*80)
# pprint(geocode_result_destination[0]['geometry']['location'])
# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
# directions_result = gmaps.distance_matrix("50.1415865,8.8984939",
# ('50.1350588,8.917969800000002',
# '50.14437,8.7201301',
# '50.121089,8.6875334'),
#     mode="driving",
# )


directions_result = gmaps.distance_matrix(origins="Händelstraße 10 Hanau Germany",
                                          destinations=['Kassel Germany', 'Freiheitsplatz Hanau Germany'],

                                          mode="driving",
                                          )

print(f"Type: {type(directions_result)}\n\n")
print(directions_result)
