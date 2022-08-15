import requests
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


class GoogleMapAPI:
    def __init__(self, query: str) -> None:
        self.query = query
        self.min_rating = 0.0
        self.max_results = 30
        self.api_key = ""
        self.s3_bucket = ""
        self.region_name = ""
        self.aws_access_key_id = ""
        self.aws_secret_access_key = ""

    def get_gmap_details(self):
        self.api_key = input("Enter your Google map API key: ")
        self.min_rating = float(
            input("Enter the lowest restaurant rating you could accept (eg: 0.0): ")
        )
        self.max_results = int(
            input("Enter the maximal number of result you want to get (eg: 30): ")
        )

    def get_aws_credentials(self):
        self.s3_bucket = input(
            "Enter your desired AWS S3 bucket name (eg:google-map-api): "
        )
        self.region_name = input("Enter AWS account region name (eg:us-east-2): ")
        self.aws_access_key_id = input("Enter aws_access_key_id: ")
        self.aws_secret_access_key = input("Enter aws_secret_access_key: ")

    def get_restaurant(self) -> List[tuple]:

        url = (
            "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s"
            % (self.query, self.api_key)
        )
        response = requests.get(url)
        try:
            response = requests.get(url)
            if not response.status_code == 200:
                print("HTTP error", response.status_code)
            else:
                try:
                    response_data = response.json()
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")

        try:
            # set next-token-page
            if (self.max_results > 20) and response_data["next_page_token"] != "":
                page_token = response_data["next_page_token"]
                new_url = (
                    "https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken=%s&key=%s"
                    % (page_token, self.api_key)
                )
                response = requests.get(new_url)
                while response.json().get("status") != "OK":
                    sleep(random())
                    response = requests.get(new_url)
                    new_response_data = response.json()
                # Add additional results from more pages when max_results is greater than 20
                response_data["results"].extend(new_response_data["results"])
        except (KeyError, TypeError) as e:
            return f"Cannot find: {e}, check if your api key is valid"

        results_ = []
        for item in response_data["results"]:
            restaurant_name = item["name"]
            address = item["formatted_address"]
            hours = item["opening_hours"]["open_now"]
            rating = item[
                "rating"
            ]  # if only take item["price_level"], no output, raise exception
            if item["rating"] >= self.min_rating:
                try:
                    price_level = item["price_level"]
                except:
                    price_level = None
            results_.append((restaurant_name, address, hours, price_level, rating))
        # look for maximum results
        if len(results_) > self.max_results:
            final_result = results_[: self.max_results]

        return final_result

    def convert_lst_to_df(self, final_result: List[tuple]) -> pd.DataFrame:
        return pd.DataFrame(
            final_result,
            columns=["name", "address", "is_opening", "price_level", "rating"],
        )

    def upload_file(
        self,
        object_name: str = None,
        file_name: str = None,
        df: pd.DataFrame = None,
        from_local_default_false: bool = False,
    ) -> bool:

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3 = boto3.resource(
            service_name="s3",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

        try:
            # import df/list directly to S3
            if from_local_default_false:
                # save dataframe as csv file to S3
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                response = s3.Object(self.s3_bucket, object_name).put(
                    Body=csv_buffer.getvalue()
                )

                status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
                if status == 200:
                    print(f"Successful S3 put_object response. Status - {status}")
                else:
                    print(f"Oops! Cannot push Dataframe to S3. Status - {status}")

            # upload a file from local to s3
            else:
                response = s3.Bucket(self.s3_bucket).upload_file(
                    Filename=file_name, Key=object_name
                )

        except ClientError as e:
            logging.error(e)
            return False
        return True


if __name__ == "__main__":
    QUERY = input("Enter Search Query: ")
    GoogleMap = GoogleMapAPI(QUERY)
    GoogleMap.get_gmap_details()
    GoogleMap.get_aws_credentials()
    result_list = GoogleMap.get_restaurant()
    result_df = GoogleMap.convert_lst_to_df(result_list)
    GoogleMap.upload_file("restaurant.csv", None, result_df, True)
    print(result_df)
