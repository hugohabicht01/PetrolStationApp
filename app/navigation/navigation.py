import googlemaps
from typing import List
from app.models import models
# from aiogmaps import Client
# import asyncio
# async def getDistanceMatrix(current_lat: str, current_lng: str, dest: List[Tuple[str, str]], api_key: str):
#     current_coords = f"{current_lat}, {current_lng}"
#     dest = [f"{dest_lat}, {dest_lng}" for dest_lat, dest_lng in dest]
#     async with Client(api_key) as client:
#         resp = await client.distance_matrix(origins=current_coords, destinations=dest)
#         return resp


def get_distance_matrix(
    current_pos: models.Coordinate, destinations: List[models.Coordinate], api_key: str,
) -> dict:
    """
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
    """
    current_coords = f"{current_pos.latitude}, {current_pos.longitude}"
    destinations = [f"{coord.latitude}, {coord.longitude}" for coord in destinations]

    gmaps = googlemaps.Client(key=api_key)

    gmaps_distance_matrix = gmaps.distance_matrix(origins=current_coords, destinations=destinations)

    if gmaps_distance_matrix['status'] != 'OK':
        raise RuntimeError('Google Maps API returned an error')

    return gmaps_distance_matrix


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
