from fastapi import FastAPI
from app.petrolprices import prices
from app.models import models
from app.navigation import navigation
from os.path import join, dirname
from os import getenv
import platform
from dotenv import load_dotenv
import uvicorn



if (os_system := platform.system()) != "Linux":
    print(
    f"""You are currently running {os_system} which is an inferior OS.
    You might want to consider switching to a superior OS.
    GNU/Linux is free (as in freedom), free (regarding the price) and will save you from many headaches.
    Start using GNU/Linux today: https://distrowatch.com/dwres.php?resource=major !"""
    )

# TODO: Consider switching to async
app = FastAPI()

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
TANKERKOENIG_API_KEY = getenv("TANKERKOENIG_API_KEY")


@app.get("/version")
async def version():
    return {"message": "Testversion, nothing works yet"}


@app.get("/find/")
def find_petrol_stations(
    lat: str,
    lng: str,
    fueltype: str,
    rad: float,
    tankfill: int,
    avg_city: float = 7.2,
    avg_motorway: float = 12,
):
    current_pos: models.Coordinate = models.Coordinate(latitude=lat, longitude=lng)
    petrol_stations: models.PetrolStations = prices.get_nearest_stations(
        current_pos, rad, fueltype, apikey=TANKERKOENIG_API_KEY
    )

    petrol_stations_nearby = navigation.find_distances_and_fuelconsumption(
        current_pos, petrol_stations, tankfill, avg_city, avg_motorway, GOOGLE_API_KEY
    )
    return {"ok": True, "petrolStations": petrol_stations_nearby}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
