from unittest import TestCase
from app.petrolprices import prices
from app.models import models
from os import getenv


class TestPriceFetching(TestCase):
    # TODO: Add proper unittests that test with failing and succeding testcases while mocking the actual API
    # TODO: Add integration tests
    def setUp(self):
        self.api_key = getenv('TANKERKOENIG_API_KEY')

    def test_get_nearest_stations(self):
        res = prices.get_nearest_stations(
            models.Coordinate(latitude='50.141593', longitude='8.898668'),
            1.5,
            "diesel",
            self.api_key
        )

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status, 'ok')
