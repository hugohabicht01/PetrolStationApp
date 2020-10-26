import requests

def getNearestStations(lat: str, lng: str, rad: float, fueltype: str, apikey: str) -> dict:
    """Fetches all petrol stations in a certain radius from a position and returns their prices"""
    PETROL_PRICES_API_URL: str = 'https://creativecommons.tankerkoenig.de/json/list.php'
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

    if prices["ok"] != "true" and prices["status"] != "ok":
        raise RuntimeError("Pricing API returned data error")

    return prices