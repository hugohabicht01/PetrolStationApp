import uuid
from pydantic import BaseModel, Field
from typing import List


class Coordinate(BaseModel):
    latitude: float
    longitude: float


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


class GMAPS(BaseModel):
    destination_addresses: List[str]
    origin_addresses: List[str]
    rows: List[Row]
    status: str
