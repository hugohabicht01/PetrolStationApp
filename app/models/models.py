import uuid
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Union


class Coordinate(BaseModel):
    """
    Coordinate datatype with latitude and longitude

    Args:
        latitude: Latitude of a coordinate
        longitude: Longitude of a coordinate
    """

    latitude: float
    longitude: float


class Fuel(BaseModel):
    fueltype: str

    @validator("fueltype")
    def check_valid_fueltype(cls, v):
        # Make sure that the fueltype is supported
        supported_fueltypes = ["diesel", "e5", "e10"]
        if v not in supported_fueltypes:
            raise ValueError("Wrong fueltype")
        return v


class Distance(BaseModel):
    text: str
    value: int


class Duration(BaseModel):
    text: str
    value: int


class Element(BaseModel):
    distance: Distance
    duration: Duration
    status: str


class Row(BaseModel):
    elements: List[Element]


class GMapsResponse(BaseModel):
    destination_addresses: List[str]
    origin_addresses: List[str]
    rows: List[Row]
    status: str


Price = Union[float, None]


class PetrolStation(BaseModel):
    id: uuid.UUID
    name: str
    brand: str
    lat: float
    lng: float
    # Might wanna use an alias for this and call this straightlinedistance
    dist: float
    price: Price
    isOpen: bool
    houseNumber: str
    postCode: int

    fuel_to_get_there: float = None
    price_to_get_there: float = None
    price_overall: float = None
    avg_speed: float = None
    distance: Distance = None
    duration: Duration = None

class OpeningTimes(BaseModel):
    text: str
    start: str
    end: str

class Details(BaseModel):
        id: str
        name: str
        brand: str
        street: str
        houseNumber: str
        postCode: str
        place: str
        openingTimes: List[OpeningTimes]
        overrides: List[str]
        wholeDay: bool
        isOpen: bool
        e5: float
        e10: float
        diesel: float
        lat: float
        lng: float
        state: Union[str, None]

class PetrolStations(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    stations: List[PetrolStation] = None
    station: Details = None


class RadiusTooBig(Exception):
    pass

class NoStationsFound(Exception):
    pass

class PricingAPIError(Exception):
    pass

class GoogleMapsError(Exception):
    pass