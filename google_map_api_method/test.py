import requests

# import sys

# sys.path.append("google-map-api-flow")
from time import sleep
from random import random
import logging
import boto3
from botocore.exceptions import ClientError
import os
from io import StringIO  # python3; python2: BytesIO
import json
from typing import List
import pandas as pd
import unittest
from secret import API_KEY, REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from api_method import GoogleMapAPI


class GoogleMapAPITest(unittest.TestCase):
    def setUp(self):
        self.query = "restaurants near Dumbo"
        self.min_rating = 0.0
        self.max_results = 30

    def test_invalid_api_key(self):
        self.api_key = "invalid_key"
        self.GoogleMap = GoogleMapAPI(self.query)
        expected_result = (
            "Cannot find: 'next_page_token', check if your api key is valid"
        )
        actual_result = self.GoogleMap.get_restaurant()
        self.assertEqual(expected_result, actual_result)

    def test_get_nonzero_result(self):
        self.api_key = API_KEY
        self.GoogleMap = GoogleMapAPI(self.query)
        expected_result = True
        actual_result = len(self.GoogleMap.get_restaurant()) > 0
        self.assertEqual(expected_result, actual_result)

    def test_invalid_aws_credential(self):
        lst = [
            (
                "restaurant1",
                "addresses1",
                True,
                2,
                4.0,
            ),
            (
                "restaurant2",
                "addresses2",
                True,
                2,
                4.0,
            ),
        ]

        df = pd.DataFrame(
            lst,
            columns=["name", "address", "is_opening", "price_level", "rating"],
        )
        self.region_name = REGION_NAME
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY

        self.GoogleMap = GoogleMapAPI(self.query)
        expected_result = True
        actual_result = self.GoogleMap.upload_file("restaurant.csv", None, df, True)

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
