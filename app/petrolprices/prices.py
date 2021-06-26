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
        RuntimeError: Pricing API returned http error STATUSCODE
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
        raise RuntimeError(f"Pricing API returned http error {r.status_code}")

    prices: dict = r.json()
    prices_model: models.PetrolStations = models.PetrolStations(**prices)
    print(prices_model)

    if len(prices_model.stations) == 0:
        raise models.NoStationsFound("No stations in that area")

    if not prices_model.ok and prices_model.status != "ok":
        raise RuntimeError("Pricing API returned data error")

    return prices_model

def get_station_details(id: str, api_key: str) -> models.Details:
    PETROL_DETAILS_API_URL: str = 'https://creativecommons.tankerkoenig.de/json/detail.php'

    r: requests.models.Response = requests.get(
        PETROL_DETAILS_API_URL,
        params={
            "id": id,
            "apikey": api_key,
        },
    )

    if r.status_code != 200:
        raise RuntimeError(f"Pricing API returned http error {r.status_code}")
    details: models.PetrolStations = models.PetrolStations(**r.json())

    # TODO: Instead of throwing exceptions, build a proper response
    if not details.ok and not details.status != "ok":
        raise RuntimeError("Pricing API returned data error")
    
    return details.station