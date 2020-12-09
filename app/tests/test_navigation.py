from unittest import TestCase
from app.navigation import navigation
from app.models import models
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv
from pprint import pprint
import responses


class TestNavigation(TestCase):
    def setUp(self):
        dotenv_path = join(dirname(__file__), ".env")
        load_dotenv(dotenv_path)
        self.api_key = getenv("GOOGLE_API_KEY")

    @responses.activate
    def test_distance_matrix(self):
        # TODO: #6 Mock the API call
        origins = models.Coordinate(latitude="50.1415865", longitude="8.8984939")

        destinations = [
            models.Coordinate(latitude="50.1350588", longitude="8.917969800000002"),
            models.Coordinate(latitude="50.14437", longitude="8.7201301"),
            models.Coordinate(latitude="50.121089", longitude="8.6875334")
        ]

        responses.add(
            responses.GET,
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            body='{"destination_addresses": ["Am Freiheitspl. 14, 63450 Hanau, Germany", "Im Staffel 109, 60389 Frankfurt am Main, Germany", "Hebelstra\\u00dfe 15, 60318 Frankfurt am Main, Germany"], "origin_addresses": ["H\\u00e4ndelstra\\u00dfe 10, 63452 Hanau, Germany"], "rows": [{"elements": [{"distance": {"text": "2.1 km", "value": 2051}, "duration": {"text": "6 mins", "value": 340}, "status": "OK"}, {"distance": {"text": "15.7 km", "value": 15710}, "duration": {"text": "19 mins", "value": 1135}, "status": "OK"}, {"distance": {"text": "20.3 km", "value": 20297}, "duration": {"text": "29 mins", "value": 1734}, "status": "OK"}]}], "status": "OK"}',
            status=200,
            content_type="application/json",
        )


        res = navigation.get_distance_matrix(origins, destinations, self.api_key).dict()
        # expected_res = {
        #     "destination_addresses": [
        #         "Am Freiheitspl. 14, 63450 Hanau, Germany",
        #         "Im Staffel 109, 60389 Frankfurt am Main, Germany",
        #         "Hebelstraße 15, 60318 Frankfurt am Main, Germany",
        #     ],
        #     "origin_addresses": ["Händelstraße 10, 63452 Hanau, Germany"],
        #     "rows": [
        #         {
        #             "elements": [
        #                 {
        #                     "distance": {"text": "2.1 km", "value": 2051},
        #                     "duration": {"text": "6 mins", "value": 340},
        #                     "status": "OK",
        #                 },
        #                 {
        #                     "distance": {"text": "15.7 km", "value": 15710},
        #                     "duration": {"text": "19 mins", "value": 1135},
        #                     "status": "OK",
        #                 },
        #                 {
        #                     "distance": {"text": "20.3 km", "value": 20297},
        #                     "duration": {"text": "29 mins", "value": 1734},
        #                     "status": "OK",
        #                 },
        #             ]
        #         }
        #     ],
        #     "status": "OK",
        # }
        # expected_res: models.GMaps_response = models.GMaps_response(
        #     destination_addresses=[
        #         "Am Freiheitspl. 14, 63450 Hanau, Germany",
        #         "Im Staffel 109, 60389 Frankfurt am Main, Germany",
        #         "Hebelstraße 15, 60318 Frankfurt am Main, Germany",
        #     ],
        #     origin_addresses=[
        #         "Händelstraße 10, 63452 Hanau, Germany"
        #     ],
        #     row=[
        #         models.Row()
        #     ],
        #     status="OK"
        # )

        print(responses.calls[0].request.url)

    def test_calculate_fuel_consumption(self):
        res_city: float = navigation.calculate_fuel_consumption(2000, 140, 10, 7)
        expected_res_city = 0.2
        self.assertEqual(res_city, expected_res_city)

        res_motorway: float = navigation.calculate_fuel_consumption(2000, 40, 10, 7)
        expected_res_motorway = 0.14
        self.assertEqual(res_motorway, expected_res_motorway)
