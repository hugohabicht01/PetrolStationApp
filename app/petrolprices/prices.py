import requests
from app.models import models


def get_nearest_stations(
    position: models.Coordinate, rad: float, fueltype: str, api_key: str
) -> models.PetrolStations:
    """
    Fetches all petrol stations in a certain radius from a position and returns their prices

    Args:
        position: current position
        rad: radius in which petrol stations should be searched for
        fueltype: fueltype of your car
        apikey: Tankerkönig API key

    Returns:
        All petrol stations within the radius

    Raises:
        models.PricingAPIError: Pricing API returned invalid data
        models.NoStationsFound: No stations were found in the given radius
    """
    PETROL_PRICES_API_URL: str = "https://creativecommons.tankerkoenig.de/json/list.php"

    lat: float = position.latitude
    lng: float = position.longitude

    r: requests.models.Response = requests.get(
        PETROL_PRICES_API_URL,
        params={
            "lat": lat,
            "lng": lng,
            "rad": rad,
            "type": fueltype,
            "apikey": api_key,
            "sort": "price",
        },
    )
    if r.status_code != 200:
        raise models.PricingAPIError

    prices: dict = r.json()

    if prices['ok'] != True or prices['status'] != "ok":
        raise models.PricingAPIError
    prices_model: models.PetrolStations = models.PetrolStations(**prices)

    if len(prices_model.stations) == 0:
        raise models.NoStationsFound("No stations in that area")

    return prices_model

def get_station_details(id: str, api_key: str) -> models.Details:
    """Fetches details about a petrol station by id
    
    Args:
        id: uuid of a petrol station
    
    Returns:
        Current petrol prices, address, opening times
    
    Raises:
        models.PricingAPIError
    """

    # TODO: Add unit- and integrationtests
    PETROL_DETAILS_API_URL: str = 'https://creativecommons.tankerkoenig.de/json/detail.php'

    r: requests.models.Response = requests.get(
        PETROL_DETAILS_API_URL,
        params={
            "id": id,
            "apikey": api_key,
        },
    )

    if r.status_code != 200:
        raise models.PricingAPIError

    res_json: dict = r.json()

    if res_json['ok'] != True or res_json['status'] != "ok":
        raise models.PricingAPIError
    
    details: models.PetrolStations = models.PetrolStations(**res_json)

    return details.station