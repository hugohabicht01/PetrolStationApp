from unittest import TestCase
from app.petrolprices import prices
from app.models import models
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv


class TestPriceFetching(TestCase):
    def setUp(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.api_key = getenv('TANKERKOENIG_API_KEY')

    def test_get_nearest_stations(self):
        res = prices.get_nearest_stations(
            models.Coordinate(latitude='50.141593', longitude='8.898668'),
            1.5,
            "diesel",
            self.api_key
        )

        self.assertEqual(res["ok"], True)
        self.assertEqual(res["status"], 'ok')
