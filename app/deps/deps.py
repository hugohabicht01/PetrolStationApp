from fastapi import HTTPException
from tankerkoenig import Petrol

from app.models import models


def getCoords(lat: str, lng: str) -> models.Coordinate:
    return models.Coordinate(latitude=lat, longitude=lng)


def parseFuelType(fueltype: str) -> Petrol:
    if fueltype == "diesel":
        return Petrol.DIESEL
    elif fueltype == "e5":
        return Petrol.E5
    elif fueltype == "e10":
        return Petrol.E10
    elif fueltype == "all":
        # TODO: Make it possible to get prices for all petrol types and not just one
        raise HTTPException(status_code=501, detail="Coming soon")
    else:
        raise HTTPException(status_code=400, detail="Bad fueltype")