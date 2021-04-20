let command = "$ curl 'localhost:8000/find/?lat=50.123&lng=8.6812&fueltype=diesel&rad=2&tankfill=30' | jq ."
let res = {
  "ok": true,
  "petrolStations": [
    {
      "id": "3a96b82f-7342-40ba-a1d7-9cde3fbb3c11",
      "name": "Aral Tankstelle",
      "brand": "ARAL",
      "lat": 50.1129227,
      "lng": 8.699732,
      "dist": 1.7,
      "price": 1.369,
      "isOpen": true,
      "houseNumber": "34-40",
      "postCode": 60314,
      "fuel_to_get_there": 0.16668000000000002,
      "price_to_get_there": 0.22818492000000004,
      "price_overall": 41.29818492,
      "avg_speed": 15.96551724137931,
      "distance": {
        "text": "2.3 km",
        "value": 2315
      },
      "duration": {
        "text": "9 mins",
        "value": 522
      }
    },
    {
      "id": "0e41a6a4-e678-4dce-8568-020210c6cee9",
      "name": "Shell Frankfurt Am Main Friedberger Landstr. 152",
      "brand": "Shell",
      "lat": 50.129887,
      "lng": 8.694316,
      "dist": 1.2,
      "price": 1.389,
      "isOpen": true,
      "houseNumber": "152",
      "postCode": 60389,
      "fuel_to_get_there": 0.10029600000000001,
      "price_to_get_there": 0.13931114400000003,
      "price_overall": 41.809311144,
      "avg_speed": 15.242553191489362,
      "distance": {
        "text": "1.4 km",
        "value": 1393
      },
      "duration": {
        "text": "5 mins",
        "value": 329
      }
    },
    {
      "id": "2fdeef9e-36ca-44d7-9ee4-3bdaa0112539",
      "name": "TOTAL Frankfurt",
      "brand": "TOTAL",
      "lat": 50.13218,
      "lng": 8.683576,
      "dist": 1,
      "price": 1.389,
      "isOpen": true,
      "houseNumber": "",
      "postCode": 60320,
      "fuel_to_get_there": 0.11268000000000002,
      "price_to_get_there": 0.15651252000000002,
      "price_overall": 41.82651252,
      "avg_speed": 15.78151260504202,
      "distance": {
        "text": "1.6 km",
        "value": 1565
      },
      "duration": {
        "text": "6 mins",
        "value": 357
      }
    },
    {
      "id": "412086bf-c3a0-4dc7-b293-d476f34a9723",
      "name": "Aral Tankstelle",
      "brand": "ARAL",
      "lat": 50.1333847,
      "lng": 8.696017,
      "dist": 1.6,
      "price": 1.399,
      "isOpen": true,
      "houseNumber": "300",
      "postCode": 60389,
      "fuel_to_get_there": 0.13147200000000003,
      "price_to_get_there": 0.18392932800000006,
      "price_overall": 42.153929328,
      "avg_speed": 15.840000000000002,
      "distance": {
        "text": "1.8 km",
        "value": 1826
      },
      "duration": {
        "text": "7 mins",
        "value": 415
      }
    },
    {
      "id": "09978ef8-5fa5-46d5-8389-957eb7cd8540",
      "name": "Aral Tankstelle",
      "brand": "ARAL",
      "lat": 50.12197,
      "lng": 8.669096,
      "dist": 0.9,
      "price": 1.429,
      "isOpen": true,
      "houseNumber": "67",
      "postCode": 60323,
      "fuel_to_get_there": 0.068832,
      "price_to_get_there": 0.09836092800000001,
      "price_overall": 42.968360928,
      "avg_speed": 13.08593155893536,
      "distance": {
        "text": "1.0 km",
        "value": 956
      },
      "duration": {
        "text": "4 mins",
        "value": 263
      }
    }
  ]
}
