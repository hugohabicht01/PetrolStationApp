from fastapi import FastAPI
from app.petrolprices import prices
from app.models import models
from app.navigation import navigation
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv
from typing import List

from pprint import pprint


# TODO: Consider switching to async
app = FastAPI()


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = getenv('GOOGLE_API_KEY')
TANKERKOENIG_API_KEY = getenv('TANKERKOENIG_API_KEY')


@app.get("/version")
async def version():
    return {"message": "Testversion, nothing works yet"}


@app.get("/find/")
def find_petrol_stations(lat: str, lng: str, fueltype: str, rad: float):
    current_pos: models.Coordinate = models.Coordinate(latitude=lat, longitude=lng)
    petrol_stations: models.PetrolStations = prices.get_nearest_stations(current_pos, rad, fueltype, apikey=TANKERKOENIG_API_KEY)


    distances = navigation.get_distance_matrix(current_pos, destinations, TANKERKOENIG_API_KEY)
    return {"ok": True, "petrolStations": petrol_stations}
