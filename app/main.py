from fastapi import FastAPI

# TODO: Consider switching to async
app = FastAPI()


@app.get("/version")
async def version():
    return {"message": "Testversion, nothing works yet"}


@app.get("/find/", status_code=501)
def find_petrol_stations(lat: str, lng: str, fueltype: str, rad: float):
    return {"ok": False, "implementationStatus": "not implemented yet"}
