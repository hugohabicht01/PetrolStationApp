from typing import List

import googlemaps
from tankerkoenig.models import List_PetrolStations

from app.models import models


def find_distances_and_fuelconsumption(
    current_pos: models.Coordinate,
    petrol_stations: List_PetrolStations,
    tankfill: float,
    avg_city_fuelconsumption: float,
    avg_motorway_fuelconsumption: float,
    api_key: str,
):
    stations_coords = []
    for station in petrol_stations.stations:
        stations_coords.append(
            models.Coordinate(latitude=station.lat, longitude=station.lng)
        )

    distances = get_distance_matrix(current_pos, stations_coords, api_key)
    stations = petrol_stations.dict()["stations"]

    return merge_pricing_navigation(
        distances=distances,
        stations=stations,
        avg_city=avg_city_fuelconsumption,
        avg_motorway=avg_motorway_fuelconsumption,
        tankfill=tankfill,
    )


def merge_pricing_navigation(*, distances, stations, avg_city, avg_motorway, tankfill):
    """
    Merge the data returned by the pricing API
    and the Gmaps directions matrix
    into one data structure
    and calculates how much the fuel
    would be used driving to the station

    Args:
        distances: Distances returned by Directions Matrix API
        stations: List of stations returned by Tankerkoenig API
        avg_city: Average fuel consumption in city traffic
        avg_motorway: Average fuel consumption on motorway
        tankfill: How many liters should get filled up

    Returns:
        Pricing and navigation data merged

    """
    stations_with_distances = []

    for i in range(len(distances)):
        # remove unnecessary status key
        distances[i].pop("status")
        station = stations[i] | distances[i]

        fuel_amounts = calculate_fuel_consumption(
            distances[i]["distance"]["value"],
            distances[i]["duration"]["value"],
            avg_city,
            avg_motorway,
        )

        price_per_liter = station["price"]

        # Price of the fuel used to drive to the station
        price_to_get_there = price_per_liter * fuel_amounts

        # Price of the fuel filled + the fuel used by driving there
        price_overall = price_to_get_there + price_per_liter * tankfill

        station["price_overall"] = price_overall

        stations_with_distances.append(models.PetrolStation(**station))

    stations_with_distances.sort(key=lambda station: station.price_overall)

    return stations_with_distances


def get_distance_matrix(
    current_pos: models.Coordinate,
    destinations: List[models.Coordinate],
    api_key: str,
) -> List[dict]:
    """
    TODO: Update this docstring
    Gets the distance matrix from the Google Maps distance matrix API

    Formats the positions and fetches the distance matrix

    Args:
        current_pos: Tuple of the latitude and longitude of the current position
        destinations: List of the destinations, these are tuples of the latitude and longitude
        api_key: Google Maps API key

    Returns:
        Response from the Google Maps API containing full address of the positions, distance, duration

    Raises:
        RuntimeError: Google Maps API returned an error

    Sample response:
        [{'distance': {'text': '3.1 km', 'value': 3133},
        'duration': {'text': '5 mins', 'value': 324},
        'status': 'OK'},
        {'distance': {'text': '5.4 km', 'value': 5392},
        'duration': {'text': '9 mins', 'value': 535},
        'status': 'OK'},
        {'distance': {'text': '5.3 km', 'value': 5298},
        'duration': {'text': '8 mins', 'value': 471},
        'status': 'OK'},
        {'distance': {'text': '3.1 km', 'value': 3085},
        'duration': {'text': '8 mins', 'value': 459},
        'status': 'OK'}]
    """
    current_coords = f"{current_pos.latitude}, {current_pos.longitude}"
    destinations = [f"{coord.latitude}, {coord.longitude}" for coord in destinations]

    gmaps = googlemaps.Client(key=api_key)

    if len(destinations) > 25:
        # TODO: Most of this (origin_addresses, status, destination_addresses)
        # is not needed, the code should be removed
        res = {
            "rows": [{"elements": []}],
        }
        for dest in _chunks(destinations, 25):
            gmaps_distance_matrix = gmaps.distance_matrix(
                origins=current_coords, destinations=dest
            )

            if gmaps_distance_matrix["status"] != "OK":
                raise RuntimeError("Google Maps API returned an error")

            res["rows"][0]["elements"].extend(
                gmaps_distance_matrix["rows"][0]["elements"]
            )
            gmaps_distance_matrix = res
    else:
        print(f"origins: {current_coords}, destinations: {destinations}")
        gmaps_distance_matrix = gmaps.distance_matrix(
            origins=current_coords, destinations=destinations
        )

        if gmaps_distance_matrix["status"] != "OK":
            raise RuntimeError("Google Maps API returned an error")

    return gmaps_distance_matrix["rows"][0]["elements"]


def calculate_fuel_consumption(
    distance: int,
    duration: int,
    avg_city_fuelconsumption: float,
    avg_motorway_fuelconsumption: float,
) -> float:
    """
    Estimates the fuel consumption of your car

    This function uses two different models, if the average speed is over 60 km/h
    it will use the average fuel consumption for motorways, otherwise the one for
    inner city traffic

    Args:
        distance: distance that is driven in meters
        duration: how long it takes to get there in seconds
        avg_city_fuelconsumption: average fuel consumption of your car in city traffic on 100km in liters
        avg_motorway_fuelconsumption: average fuel consumption of your car on a motorway on 100km in liters

    Returns:
        Estimated fuel consumed in liters
    """
    # Get the avg. consumption on 1 km
    avg_city_fuelconsumption /= 100
    avg_motorway_fuelconsumption /= 100

    # Find speed in m/s and convert it to km/h
    speed: float = (distance / duration) * 3.6

    if speed >= 60:
        return (distance / 1000) * avg_motorway_fuelconsumption
    return (distance / 1000) * avg_city_fuelconsumption


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i: i + n]
