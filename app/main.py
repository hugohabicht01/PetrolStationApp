from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.petrolprices import prices
from app.models import models
from app.navigation import navigation
from os.path import join, dirname
import sys
from dotenv import dotenv_values


# TODO: Consider switching to async
app = FastAPI()
print("fastapi started")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_keys = dotenv_values(join(dirname(__file__), ".env"))

try:
    GOOGLE_API_KEY = api_keys['GOOGLE_API_KEY']
    TANKERKOENIG_API_KEY = api_keys['TANKERKOENIG_API_KEY']
    print("loaded api keys")
except KeyError:
    print("Not all API keys were supplied, exiting")
    sys.exit(1)
# TODO: Add validation that it actually loaded API keys


@app.get("/version")
async def version():
    print("Hit route /version")
    return {"version": "0.1", "status":"working but not everything is implemented yet"}

# TODO: Implement route that returns details about a petrol station by UUID
# See https://creativecommons.tankerkoenig.de/ for more information
@app.get("/details")
def details_petrol_station(id: str):
    return {"ok": True, "details": prices.get_station_details(id, TANKERKOENIG_API_KEY)}


@app.get("/find")
def find_petrol_stations(
    lat: str,
    lng: str,
    fueltype: str,
    rad: float,
    tankfill: int,
    avg_city: float = 12,
    avg_motorway: float = 7.2,
):
    current_pos: models.Coordinate = models.Coordinate(latitude=lat, longitude=lng)
    try:
        petrol_stations: models.PetrolStations = prices.get_nearest_stations(
            current_pos, rad, fueltype, api_key=TANKERKOENIG_API_KEY
        )
    except models.NoStationsFound:
        raise HTTPException(
            status_code=400,
            detail="No stations in this area, try increasing the radius",
        )

    # TODO: Refractor this and implement some kind of pagination to allow for higher search radii
    try:
        petrol_stations_nearby = navigation.find_distances_and_fuelconsumption(
            current_pos,
            petrol_stations,
            tankfill,
            avg_city,
            avg_motorway,
            GOOGLE_API_KEY,
        )
    except models.GoogleMapsError:
        raise HTTPException(
            status_code=400,
            detail="Error finding navigation details, please search with changed parameters",
        )
    return {"ok": True, "petrolStations": petrol_stations_nearby}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
