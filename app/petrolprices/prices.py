import requests
from app.models import models


def get_nearest_stations(positon: models.Coordinate, rad: float, fueltype: str, apikey: str) -> models.PetrolStations:
    """
    Fetches all petrol stations in a certain radius from a position and returns their prices

    Args:
        positon: current position
        rad: radius in which petrol stations should be searched for
        fueltype: fueltype of your car
        apikey: Tankerkönig API key

    Returns:
        All petrol stations within the radius

    Raises:
        RuntimeError: Pricing API returned http error STATUSCODE
    """
    PETROL_PRICES_API_URL: str = 'https://creativecommons.tankerkoenig.de/json/list.php'

    lat: float = positon.latitude
    lng: float = positon.longitude

    r: requests.models.Response = requests.get(PETROL_PRICES_API_URL,
                                               params={"lat": lat,
                                                       "lng": lng,
                                                       "rad": rad,
                                                       "type": fueltype,
                                                       "apikey": apikey,
                                                       "sort": "price"
                                                       }
                                               )
    if r.status_code != 200:
        raise RuntimeError(f"Pricing API returned http error {r.status_code}")

    prices: dict = r.json()

    prices_model: models.PetrolStations = models.PetrolStations(**prices)
    if not prices_model.ok and prices_model.status != "ok":
        raise RuntimeError("Pricing API returned data error")

    return prices_model
