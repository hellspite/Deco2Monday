# Manages the Deco part of the app

import requests
import os
from datetime import datetime, date, timedelta

USERNAME = os.environ["DECO_USER"]
PASSWORD = os.environ["DECO_PASS"]
API_URL = "https://straighttohell.eu/api/json/manage_orders/find"


def is_monday(today):
    """Return a boolean

    Checks if today is monday
    """

    if today.weekday() == 0:
        return True
    else:
        return False


def clean_orders(response_json):
    """Return a list

    Select orders that are not already programmed.
    """
    cleans = []
    print(len(response_json["orders"]))
    for order in response_json["orders"]:
        lines_to_do = False
        for line in order["order_lines"]:
            try:
                if line["production_assigned_to"]["firstname"] is not None:
                    print(line["production_assigned_to"]["firstname"])
            except TypeError as error:
                lines_to_do = True
                print(error)
            else:
                if line["production_assigned_to"]["firstname"] != "Nicola":
                    lines_to_do = True

        if lines_to_do:
            cleans.append(order)

    return cleans


def get_orders():
    """Return a list of orders

    Retrieves the data of the orders from Deco API
    """

    # Retrieve today's date at midnight
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    if is_monday(today):
        start_date = date.today() - timedelta(days=3)
    else:
        start_date = date.today() - timedelta(days=1)

    start_date_formatted = start_date.strftime("%Y-%m-%dT00:00:00")

    params = {
        "field": "1",
        "condition": "6",
        "date1": start_date_formatted,
        "username": USERNAME,
        "password": PASSWORD
    }

    response = requests.get(API_URL, params=params)
    orders = clean_orders(response.json())

    return orders
