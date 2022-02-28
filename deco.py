# Manages the Deco part of the app

import requests
import os
from datetime import datetime, date, timedelta

USERNAME = os.environ["DECO_USER"]
PASSWORD = os.environ["DECO_PASS"]
API_URL = "https://straighttohell.eu/api/json/manage_orders/find"


def get_orders():

    # Retrieve yesterday's and today's date at midnight
    yesterday = date.today() - timedelta(days=1)
    yesterday_formatted = yesterday.strftime("%Y-%m-%dT00:00:00")
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today_formatted = today.strftime("%Y-%m-%dT%H:%M:%S")

    # TODO if it's monday select orders from two days ago
    # TODO if it's midweek select orders from yesterday

    params = {
        "field": "1",
        "condition": "6",
        "date1": yesterday_formatted,
        "username": USERNAME,
        "password": PASSWORD
    }

    response = requests.get(API_URL, params=params)

    print(response.json()["orders"])
