from os import getenv
from typing import List

import googlemaps
import tankerkoenig
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.deps import deps
from app.models import models
from app.navigation import navigation

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


@app.get("/details", response_model=tankerkoenig.models.Details_Station)
def details_petrol_station(id: str):
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


@app.get("/find", response_model=models.Find_Result)
def find_petrol_stations(
    rad: float,
    tankfill: int,
    avg_city: float = 12,
    avg_motorway: float = 7.2,
    current_pos: models.Coordinate = Depends(deps.getCoords),
    petrol_type: tankerkoenig.Petrol = Depends(deps.parseFuelType),
) -> models.Find_Result:

    try:
        # TODO: In the tankerkoenig lib, make it possible to get the raw json and not the model
        petrol_stations = pricingClient.list(
            lat=current_pos.latitude,
            lng=current_pos.longitude,
            rad=rad,
            petrol_type=petrol_type,
            sort=tankerkoenig.SortingMethod.PRICE,
        )

        if len(petrol_stations.stations) == 0:
            return petrol_stations
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
    except googlemaps.exceptions.ApiError as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error finding navigation details, please search with changed parameters",
        )

    return models.Find_Result(ok=True, petrolStations=petrol_stations_nearby)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
