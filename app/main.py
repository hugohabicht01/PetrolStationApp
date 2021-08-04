from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tankerkoenig
from app.models import models
from app.navigation import navigation
from os import getenv


app = FastAPI()
print("fastapi started")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# dotenv not needed as pipenv already loads the variables from .env
# in codespaces it will be available as a normal environment variable from
# codespaces secrets
GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
TANKERKOENIG_API_KEY = getenv("TANKERKOENIG_API_KEY")

pricingClient = tankerkoenig.Client(api_key=TANKERKOENIG_API_KEY)


@app.get("/version")
async def version():
    return {"version": "0.1", "status": "working but not everything is implemented yet"}


@app.get("/details")
def details_petrol_station(id: str):
    # TODO: Add proper errorhandling, this is very hacky...
    # Some more verbosity would also be nice so that the response makes clear
    # if the error occured
    # on the server side or if its just a bad request
    # TODO: Return a model instead of a dict

    try:
        return {
            "ok": True,
            # "details": prices.get_station_details(id, TANKERKOENIG_API_KEY),
            "details": pricingClient.details(id=id).station,
        }
    except tankerkoenig.exceptions.bad_id as e:
        raise HTTPException(status_code=400, detail=e)
    except tankerkoenig.exceptions.api_error as e:
        raise HTTPException(status_code=400, detail=e)


@app.get("/find")
def find_petrol_stations(
    lat: str,
    lng: str,
    fueltype: str,
    rad: float,
    tankfill: int,
    avg_city: float = 12,
    avg_motorway: float = 7.2,
) -> models.Find_Result:

    # TODO: Make this a function and inject this instead
    current_pos: models.Coordinate = models.Coordinate(latitude=lat, longitude=lng)

    # TODO: Make this a function and inject this instead
    if fueltype == "diesel":
        petrol_type = tankerkoenig.Petrol.DIESEL
    elif fueltype == "e5":
        petrol_type = tankerkoenig.Petrol.E5
    elif fueltype == "e10":
        petrol_type = tankerkoenig.Petrol.E10
    elif fueltype == "all":
        # TODO: Make it possible to get prices for all petrol types and not just one
        raise HTTPException(status_code=501, detail="Coming soon")
        # petrol_type = tankerkoenig.Petrol.ALL
    else:
        raise HTTPException(status_code=400, detail="Bad fueltype")

    try:
        # TODO: In the tankerkoenig lib, make it possible to get the raw json and not the model
        petrol_stations = pricingClient.list(
            lat=lat,
            lng=lng,
            rad=rad,
            petrol_type=petrol_type,
            sort=tankerkoenig.SortingMethod.PRICE,
        )
    except (
        tankerkoenig.exceptions.bad_latitude,
        tankerkoenig.exceptions.bad_longitude,
    ) as e:
        raise HTTPException(status_code=400, detail=e)
    except tankerkoenig.exceptions.bad_radius:
        raise HTTPException(status_code=400, detail="Bad radius")
    except tankerkoenig.exceptions.api_error as e:
        raise HTTPException(status_code=400, detail=e)

    try:
        petrol_stations_nearby: List[
            models.PetrolStation
        ] = navigation.find_distances_and_fuelconsumption(
            current_pos,
            petrol_stations,
            tankfill,
            avg_city,
            avg_motorway,
            GOOGLE_API_KEY,
        )
    # TODO: Figure out when this exception gets triggered
    # Just noticed that it didn't exist in the models, that's why I'm kind of confused...
    # Added it to prevent errors but knowing the origin would be handy
    except models.GoogleMapsError as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error finding navigation details, please search with changed parameters",
        )

    return models.Find_Result(ok=True, petrolStations=petrol_stations_nearby)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
