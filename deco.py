# Manages the Deco part of the app

import requests
from datetime import datetime, date, timedelta

USERNAME = ""
PASSWORD = ""
API_URL = "https://straighttohell.eu/api/json/manage_orders/find"

# Retrieve yesterday's and today's date at midnight
yesterday = date.today() - timedelta(days=1)
yesterday_formatted = yesterday.strftime("%Y-%m-%dT00:00:00")
today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
today_formatted = today.strftime("%Y-%m-%dT%H:%M:%S")

params = {
    "field": "1",
    "condition": "6",
    "date1": yesterday_formatted,
    "username": USERNAME,
    "password": PASSWORD
}

print(yesterday_formatted)

response = requests.get(API_URL, params=params)

print(response.json()["orders"])
