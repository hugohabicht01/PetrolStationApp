import googlemaps
from typing import List
from app.models import models
import operator


def find_distances_and_fuelconsumption(
        current_pos: models.Coordinate,
        petrol_stations: models.PetrolStations,
        tankfill: float,
        avg_city_fuelconsumption: float,
        avg_motorway_fuelconsumption: float,
        api_key: str,
):
    """TODO: Finish the function"""
    #  TODO: This whole
    #  function is extremly ugly and bad code, PLS CLEAN THIS UP FFS Just add some classes and do all the stations
    #  thingies object oriented, will be way cleaner than this mess Whoever this reads, sorry for the offensive
    #  language, but programming can sometimes make us all a bit salty if not everything is working how we want it to
    #  work

    # TODO: Although I hate myself for doing this, to just get something working, I'm gonna set this constant
    # THIS NEEDS A WAY OF CHANGING IT. YOU DONT ALWAYS WANT TO FILL UP 10 LITERS!!!

    stations_coords = []
    for station in petrol_stations.stations:
        stations_coords.append(models.Coordinate(latitude=station.lat, longitude=station.lng))

    distances: models.GMapsResponse = get_distance_matrix(
        current_pos, stations_coords, api_key
    )

    for i, nav_station in enumerate(distances.rows[0].elements):
        # Assign the real distance, not what the Tankerkoenig api returned, that is the straight line distance
        petrol_stations.stations[i].distance = nav_station.distance
        # Journey time
        petrol_stations.stations[i].duration = nav_station.duration

        petrol_stations.stations[i].fuel_to_get_there, petrol_stations.stations[i].avg_speed = calculate_fuel_consumption(
            petrol_stations.stations[i].distance.value,
            petrol_stations.stations[i].duration.value,
            avg_city_fuelconsumption,
            avg_motorway_fuelconsumption,
        )

        petrol_stations.stations[i].price_to_get_there = petrol_stations.stations[i].price * petrol_stations.stations[
            i].fuel_to_get_there
        # Calculate how much you would spend in case you would fill your tank at that station
        petrol_stations.stations[i].price_overall = petrol_stations.stations[i].price_to_get_there + \
                                                    petrol_stations.stations[i].price * tankfill

    petrol_stations_sorted = sorted(petrol_stations.stations, key=operator.attrgetter('price_overall'))

    return petrol_stations_sorted


def get_distance_matrix(
        current_pos: models.Coordinate,
        destinations: List[models.Coordinate],
        api_key: str,
) -> models.GMapsResponse:
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

    gmaps_distance_matrix = gmaps.distance_matrix(
        origins=current_coords, destinations=destinations
    )

    gmaps_distance_matrix_model = models.GMapsResponse(**gmaps_distance_matrix)

    if gmaps_distance_matrix_model.status != "OK":
        raise RuntimeError("Google Maps API returned an error")

    return gmaps_distance_matrix_model


def calculate_fuel_consumption(
        distance: int,
        duration: int,
        avg_city_fuelconsumption: float,
        avg_motorway_fuelconsumption: float,
) -> (float, float):
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
        Average speed in km/h
    """
    # Get the avg. consumption on 1 km
    avg_city_fuelconsumption /= 100
    avg_motorway_fuelconsumption /= 100

    # Find speed in m/s and convert it to km/h
    speed: float = (distance / duration) * 3.6

    if speed >= 60:
        return (distance / 1000) * avg_motorway_fuelconsumption, speed
    return (distance / 1000) * avg_city_fuelconsumption, speed
