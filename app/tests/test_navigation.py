from os import getenv
from unittest import TestCase

import responses

from app.models import models
from app.navigation import navigation


class TestNavigation(TestCase):
    def setUp(self):
        self.api_key = getenv("GOOGLE_API_KEY")

    @responses.activate
    def test_distance_matrix(self):
        origins = models.Coordinate(latitude="50.1415865", longitude="8.8984939")

        destinations = [
            models.Coordinate(latitude="50.1350588", longitude="8.917969800000002"),
            models.Coordinate(latitude="50.14437", longitude="8.7201301"),
            models.Coordinate(latitude="50.121089", longitude="8.6875334"),
        ]

        responses.add(
            responses.GET,
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            body='{"destination_addresses": ["Am Freiheitspl. 14, 63450 Hanau, Germany", "Im Staffel 109, 60389 Frankfurt am Main, Germany", "Hebelstra\\u00dfe 15, 60318 Frankfurt am Main, Germany"], "origin_addresses": ["H\\u00e4ndelstra\\u00dfe 10, 63452 Hanau, Germany"], "rows": [{"elements": [{"distance": {"text": "2.1 km", "value": 2051}, "duration": {"text": "6 mins", "value": 340}, "status": "OK"}, {"distance": {"text": "15.7 km", "value": 15710}, "duration": {"text": "19 mins", "value": 1135}, "status": "OK"}, {"distance": {"text": "20.3 km", "value": 20297}, "duration": {"text": "29 mins", "value": 1734}, "status": "OK"}]}], "status": "OK"}',
            status=200,
            content_type="application/json",
        )

        _ = navigation.get_distance_matrix(origins, destinations, self.api_key)
        # clean the url from the api key
        accessed_url = responses.calls[0].request.url
        accessed_url = accessed_url[:accessed_url.find("&key")]
        self.assertEqual(
            accessed_url,
            "https://maps.googleapis.com/maps/api/distancematrix/json?destinations=50.1350588%2C+8.917969800000002%7C50.14437%2C+8.7201301%7C50.121089%2C+8.6875334&origins=50.1415865%2C+8.8984939",
        )

    def test_calculate_fuel_consumption(self):
        res_city = navigation.calculate_fuel_consumption(
            distance=2000,
            duration=140,
            avg_city_fuelconsumption=10,
            avg_motorway_fuelconsumption=7,
        )
        expected_res_city = 0.2
        self.assertEqual(res_city, expected_res_city)

        res_motorway = navigation.calculate_fuel_consumption(
            distance=2000,
            duration=40,
            avg_city_fuelconsumption=10,
            avg_motorway_fuelconsumption=7,
        )
        expected_res_motorway = 0.14
        self.assertEqual(res_motorway, expected_res_motorway)
