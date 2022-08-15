import unittest
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


if __name__ == "__main__":
    unittest.main()
