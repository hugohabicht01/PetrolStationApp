from unittest import TestCase
from app.navigation import navigation
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv


class TestNavigation(TestCase):
    def setUp(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.api_key = getenv('GOOGLE_API_KEY')

    def test_distance_matrix(self):
        origins = ("50.1415865", "8.8984939")

        destinations = [
            ('50.1350588', '8.917969800000002'),
            ('50.14437', '8.7201301'),
            ('50.121089', '8.6875334')
        ]

        res = navigation.getDistanceMatrix(origins, destinations, self.api_key)
        expected_res = {'destination_addresses': ['Am Freiheitspl. 14, 63450 Hanau, Germany', 'Im Staffel 109, 60389 Frankfurt am Main, Germany', 'Hebelstraße 15, 60318 Frankfurt am Main, Germany'], 'origin_addresses': ['Händelstraße 10, 63452 Hanau, Germany'], 'rows': [{'elements': [{'distance': {'text': '2.1 km', 'value': 2051}, 'duration': {'text': '6 mins', 'value': 340}, 'status': 'OK'}, {'distance': {'text': '15.7 km', 'value': 15710}, 'duration': {'text': '19 mins', 'value': 1135}, 'status': 'OK'}, {'distance': {'text': '20.3 km', 'value': 20297}, 'duration': {'text': '29 mins', 'value': 1734}, 'status': 'OK'}]}], 'status': 'OK'}
        self.assertEqual(res, expected_res)
        print(res)
        