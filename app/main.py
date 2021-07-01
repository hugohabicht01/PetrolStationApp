from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.petrolprices import prices
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
# in codespaces it will be available as a normal environment variable from codespaces secrets
GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
TANKERKOENIG_API_KEY = getenv("TANKERKOENIG_API_KEY")

@app.get("/version")
async def version():
    print("Hit route /version")
    return {"version": "0.1", "status":"working but not everything is implemented yet"}

@app.get("/details")
def details_petrol_station(id: str):
    # TODO: Add proper errorhandling, this is very hacky...
    # Some more verbosity would also be nice so that the response makes clear if the error occured 
    # on the server side or if its just a bad request

    try:
        return {"ok": True, "details": prices.get_station_details(id, TANKERKOENIG_API_KEY)}
    except models.PricingAPIError:
        return {"ok": False, "details": "Bad request"}


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
    # TODO: Figure out when this exception gets triggered
    # Just noticed that it didn't exist in the models, that's why I'm kind of confused...
    # Added it to prevent errors but knowing the origin would be handy
    except models.GoogleMapsError as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error finding navigation details, please search with changed parameters",
        )
    return {"ok": True, "petrolStations": petrol_stations_nearby}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
