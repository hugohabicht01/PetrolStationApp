import googlemaps
import re
from typing import List, Tuple


# from aiogmaps import Client
# import asyncio
# async def getDistanceMatrix(current_lat: str, current_lng: str, dest: List[Tuple[str, str]], api_key: str):
#     current_coords = f"{current_lat}, {current_lng}"
#     dest = [f"{dest_lat}, {dest_lng}" for dest_lat, dest_lng in dest]
#     async with Client(api_key) as client:
#         resp = await client.distance_matrix(origins=current_coords, destinations=dest)
#         return resp


def get_distance_matrix(
    current_pos: Tuple[str, str], destinations: List[Tuple[str, str]], api_key: str,
) -> dict:
    current_coords = f"{current_pos[0]}, {current_pos[1]}"
    destinations = [f"{dest_lat}, {dest_lng}" for dest_lat, dest_lng in destinations]

    gmaps = googlemaps.Client(key=api_key)

    return gmaps.distance_matrix(origins=current_coords, destinations=destinations)


def calculate_fuel_consumption(
    distance: float,
    duration: str,
    avg_city_fuelconsumption: float,
    avg_motorway_fuelconsumption: float,
) -> float:
    """
    @param: distance, distance that is driven
    @param: duration, how long it takes to get there, format: "x hours y mins"
    @param: avg_city_fuelconsumption: average fuel consumption of your car in city traffic on 100km in liters
    @param: avg_motorway_fuelconsumption: average fuel consumption of your car on a motorway on 100km in liters

    This function uses two different models, if the average speed is over 60 km/h
    it will use the average fuel consumption for motorways, otherwise the one for 
    inner city traffic
    """
    # TODO: Add test
    # Get the avg. consumption on 1 km
    avg_city_fuelconsumption /= 100
    avg_motorway_fuelconsumption /= 100

    # Convert
    speed: float = distance / _parse_gmaps_travelduration(duration)

    if speed >= 60:
        return distance * avg_motorway_fuelconsumption
    return distance * avg_city_fuelconsumption


def _parse_gmaps_travelduration(duration: str) -> float:
    """
    Possible formats(not real regular expressions!!!!!): [1-59] mins? || [1-23] hours [0-59] mins?
    Returns the time in hours
    """
    # TODO: Add test
    total_hours: float = 0

    # Find the hours if existent
    if duration.find("hour") != -1:
        hours: int = int(re.search("([1-9][0-9]?) hours?", duration).group(1))
        # Check for impossible results
        if hours >= 24:
            raise ValueError("Faulty duration")

        total_hours += hours

    # Find the minutes
    minutes: int = int(re.search("([0-9][0-9]?) mins?", duration).group(1))

    # Convert minutes to hours and add to total
    # TODO: For docs, there is no need to account for minutes higher than 59,
    # it can't overflow
    total_hours += minutes / 60

    return total_hours
