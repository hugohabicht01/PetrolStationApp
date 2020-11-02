import uuid
from typing import List

from pydantic import BaseModel


class Coordinate(BaseModel):
    latitude: float
    longitude: float


# {
#     "ok": true,
#     "petrolStations": {
#         "ok": true,
#         "license": "CC BY 4.0 -  https://creativecommons.tankerkoenig.de",
#         "data": "MTS-K",
#         "status": "ok",
#         "stations": [
#             {
#                 "id": "7d0c575c-f3c0-402c-b03a-3ccca769446b",
#                 "name": "bft-Tankstelle Förster, Hanau",
#                 "brand": "bft",
#                 "street": "Brüder-Grimm-Str.",
#                 "place": "Hanau",
#                 "lat": 50.1277,
#                 "lng": 8.91757,
#                 "dist": 2.1,
#                 "price": 0.989,
#                 "isOpen": true,
#                 "houseNumber": "24",
#                 "postCode": 63450
#             },
#             {
#                 "id": "51d4b4e3-a095-1aa0-e100-80009459e03a",
#                 "name": "JET HANAU WESTERBURGSTR. 7",
#                 "brand": "JET",
#                 "street": "WESTERBURGSTR. 7",
#                 "place": "HANAU",
#                 "lat": 50.124559,
#                 "lng": 8.914755,
#                 "dist": 2.2,
#                 "price": 0.989,
#                 "isOpen": true,
#                 "houseNumber": "",
#                 "postCode": 63450
#             },
#             {
#                 "id": "8b97dd5e-6411-48bf-8fb0-93f5c3f2b0c9",
#                 "name": "Günel Gürsel",
#                 "brand": "bft - Walther",
#                 "street": "Luise-Kiesselbach-Str.",
#                 "place": "Hanau",
#                 "lat": 50.146823,
#                 "lng": 8.930002,
#                 "dist": 2.3,
#                 "price": 0.989,
#                 "isOpen": true,
#                 "houseNumber": "3",
#                 "postCode": 63452
#             },
#             {
#                 "id": "6606780d-c62d-4285-93f1-0e34f54234e7",
#                 "name": "Aral Tankstelle",
#                 "brand": "ARAL",
#                 "street": "Friedrich-Ebert-Anlage",
#                 "place": "Hanau",
#                 "lat": 50.1297,
#                 "lng": 8.921511,
#                 "dist": 2.1,
#                 "price": 0.999,
#                 "isOpen": true,
#                 "houseNumber": "7",
#                 "postCode": 63450
#             },
#             {
#                 "id": "b4d9b683-6452-430e-9f59-3482cce5a9a2",
#                 "name": "Calpam Tankstelle",
#                 "brand": "Calpam",
#                 "street": "Lamboystr",
#                 "place": "Hanau",
#                 "lat": 50.14123916626,
#                 "lng": 8.929069519043,
#                 "dist": 2.2,
#                 "price": 0.999,
#                 "isOpen": true,
#                 "houseNumber": "10",
#                 "postCode": 63452
#             },
#             {
#                 "id": "7bb46356-16ee-487e-bed2-a94b501fca20",
#                 "name": "Shell Hanau Offenbacher Landstr. 25",
#                 "brand": "Shell",
#                 "street": "Offenbacher Landstr.",
#                 "place": "Hanau",
#                 "lat": 50.122548,
#                 "lng": 8.903817,
#                 "dist": 2.2,
#                 "price": 1.009,
#                 "isOpen": true,
#                 "houseNumber": "25",
#                 "postCode": 63456
#             },
#             {
#                 "id": "5a2ca51f-d09a-46da-8c4d-d87158de2200",
#                 "name": "Aral Tankstelle",
#                 "brand": "ARAL",
#                 "street": "Maintaler Straße",
#                 "place": "Hanau",
#                 "lat": 50.147583,
#                 "lng": 8.901271,
#                 "dist": 0.7,
#                 "price": 1.029,
#                 "isOpen": true,
#                 "houseNumber": "20",
#                 "postCode": 63452
#             },
#             {
#                 "id": "dc92d9f0-0fd7-4640-a5e7-1042be447104",
#                 "name": "HANAU, BRUCHKÖBELER LANDSTRASSE",
#                 "brand": "Agip",
#                 "street": "Bruchkoebeler Landstrasse",
#                 "place": "Hanau",
#                 "lat": 50.1458853,
#                 "lng": 8.9091131,
#                 "dist": 0.9,
#                 "price": 1.029,
#                 "isOpen": true,
#                 "houseNumber": "53",
#                 "postCode": 63452
#             },
#             {
#                 "id": "45317f68-3d4c-46a4-a90e-2a6d33d2ceec",
#                 "name": "Esso Tankstelle",
#                 "brand": "ESSO",
#                 "street": "KLEINE HAINSTR. 4",
#                 "place": "HANAU",
#                 "lat": 50.138068,
#                 "lng": 8.913194,
#                 "dist": 1.1,
#                 "price": 1.029,
#                 "isOpen": true,
#                 "houseNumber": "",
#                 "postCode": 63450
#             }
#         ]
#     }
# }


# {
#                 "id": "7d0c575c-f3c0-402c-b03a-3ccca769446b",
#                 "name": "bft-Tankstelle Förster, Hanau",
#                 "brand": "bft",
#                 "street": "Brüder-Grimm-Str.",
#                 "place": "Hanau",
#                 "lat": 50.1277,
#                 "lng": 8.91757,
#                 "dist": 2.1,
#                 "price": 0.989,
#                 "isOpen": true,
#                 "houseNumber": "24",
#                 "postCode": 63450
#             },

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
