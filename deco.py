# Manages the Deco part of the app
from dotenv import load_dotenv
import requests
import os
from datetime import date, timedelta

load_dotenv()

USERNAME = os.getenv("DECO_USER")
PASSWORD = os.getenv("DECO_PASS")
API_URL = "https://merchandising.straighttohell.eu/api/json/manage_orders/find"


def clean_orders(response_json):
    """Return a list

    Select orders that are not already programmed.
    """
    cleans = []

    # print(len(response_json["orders"]))
    for order in response_json["orders"]:
        print(f"Processing order {order['order_id']}")

        lines_to_do = False
        lines_num = len(order["order_lines"])
        line = order["order_lines"][0]

        try:
            if line["production_assigned_to"]["firstname"] != "Nicola":
                lines_to_do = True
        except (TypeError, KeyError) as error:
            if lines_num > 1:
                line2 = order["order_lines"][1]
                try:
                    if line2["production_assigned_to"] is None:
                        lines_to_do = True
                    elif line2["production_assigned_to"]["firstname"] == "Nicola":
                        lines_to_do = False
                except (TypeError, KeyError) as error:
                    lines_to_do = True
            else:
                lines_to_do = True
            print(f"TypeError on order {order['order_id']}")

        # Check if it's a Tribe Jiu Jitsu order
        if order["store"]["owner"]["company"] == "tribejiujitsushop":
            lines_to_do = False

        # if orders are still quotes or if they have been cancelled
        # don't include them in the list
        if order["order_status"] == 7 or order["order_status"] == 4:
            print(f"Order {order['order_id']} cancelled or blocked")
            lines_to_do = False

        if lines_to_do:
            print(f"Order {order['order_id']} added")
            cleans.append(order)

    return cleans


def get_orders(days_back):
    """Return a list of orders

    Retrieve the data of the orders from Deco API
    """

    start_date = date.today() - timedelta(days_back)

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
