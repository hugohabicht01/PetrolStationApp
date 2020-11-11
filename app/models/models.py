import uuid
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List


class Coordinate(BaseModel):
    latitude: float
    longitude: float

class Fuel(BaseModel):
    fueltype: str

    @validator('fueltype')
    def check_valid_fueltype(cls, v):
        if v != 'diesel' or v != 'e5' or v != 'e10':
            raise ValueError('Wrong fueltype')
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


class GMaps_response(BaseModel):
    destination_addresses: List[str]
    origin_addresses: List[str]
    rows: List[Row]
    status: str


class PetrolStation(BaseModel):
    id: uuid.UUID
    name: str
    brand: str
    lat: float
    lng: float
    dist: float
    price: float
    isOpen: bool
    houseNumber: str
    postCode: int



class PetrolStations(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    stations: List[PetrolStation]

