import googlemaps
from typing import List, Tuple
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
    # TODO: This whole function is extremly ugly and bad code.
    # Just add some classes and do all the stations
    # object oriented, will be way cleaner than this mess

    stations_coords = []
    for station in petrol_stations.stations:
        stations_coords.append(
            models.Coordinate(latitude=station.lat, longitude=station.lng)
        )

    distances: models.GMapsResponse = get_distance_matrix(
        current_pos, stations_coords, api_key
    )

    for i, nav_station in enumerate(distances.rows[0].elements):
        # Assign the real distance, not what the Tankerkoenig api returned, that is the straight line distance
        petrol_stations.stations[i].distance = nav_station.distance
        # Journey time
        petrol_stations.stations[i].duration = nav_station.duration

        fuel_amounts, avg_speed = calculate_fuel_consumption(
            petrol_stations.stations[i].distance.value,
            petrol_stations.stations[i].duration.value,
            avg_city_fuelconsumption,
            avg_motorway_fuelconsumption,
        )

        petrol_stations.stations[i].fuel_to_get_there = fuel_amounts
        petrol_stations.stations[i].avg_speed = avg_speed

        petrol_stations.stations[i].price_to_get_there = (
            petrol_stations.stations[i].price
            * petrol_stations.stations[i].fuel_to_get_there
        )
        # Calculate how much you would spend in case you would fill your tank at that station
        petrol_stations.stations[i].price_overall = (
            petrol_stations.stations[i].price_to_get_there
            + petrol_stations.stations[i].price * tankfill
        )

    petrol_stations_sorted = sorted(
        petrol_stations.stations, key=operator.attrgetter("price_overall")
    )

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

    if len(destinations) > 25:
        res = {
            "destination_addresses": [],
            "rows": [{"elements": []}],
            "origin_addresses": [],
            "status": "",
        }
        for dest in _chunks(destinations, 25):
            gmaps_distance_matrix = gmaps.distance_matrix(
                origins=current_coords, destinations=dest
            )

            if gmaps_distance_matrix["status"] != "OK":
                raise RuntimeError("Google Maps API returned an error")

            # TODO: Only do once
            res["status"] = "OK"
            res["origin_addresses"] = gmaps_distance_matrix["origin_addresses"]

            res["destination_addresses"].extend(
                gmaps_distance_matrix["destination_addresses"]
            )
            res["rows"][0]["elements"].extend(
                gmaps_distance_matrix["rows"][0]["elements"]
            )
            gmaps_distance_matrix = res
    else:
        gmaps_distance_matrix = gmaps.distance_matrix(
            origins=current_coords, destinations=destinations
        )

        if gmaps_distance_matrix["status"] != "OK":
            raise RuntimeError("Google Maps API returned an error")

    gmaps_distance_matrix_model = models.GMapsResponse(**gmaps_distance_matrix)

    return gmaps_distance_matrix_model


def calculate_fuel_consumption(
    distance: int,
    duration: int,
    avg_city_fuelconsumption: float,
    avg_motorway_fuelconsumption: float,
) -> Tuple[float, float]:
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


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
