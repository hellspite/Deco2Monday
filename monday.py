from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

API_URL = "https://api.monday.com/v2"
API_KEY = os.getenv("MONDAY_API")
BOARD_ID = "2241731758"
GROUP_ID = "nuovo_gruppo74198"
headers = {"Authorization": API_KEY, "API-Version": "2023-10"}


def test_query():

    # query = '{ boards (ids: 2241731758) {name id description items{name group{id}}} }'

    query = '{ boards (ids: 2241731758) {columns {id title}} }'

    data = {'query': query}

    response = requests.post(url=API_URL, json=data, headers=headers)

    print(response.json())


def check_deco_group():
    """Return list

    Get the order ids of the orders already in the Deco Group on Monday
    """
    query = '{ boards (ids: 2241731758) {items_page{ cursor items {name, group{id}}} }}'

    data = {'query': query}

    response = requests.post(url=API_URL, json=data, headers=headers)
    orders = response.json()["data"]["boards"][0]["items_page"]["items"]
    cursor = response.json()["data"]["boards"][0]["items_page"]["cursor"]

    while cursor:
        query = "{ next_items_page (limit: 100, cursor: \"" + cursor + "\") { cursor items {name, group{id}} }}"
        data = {'query': query}
        response = requests.post(url=API_URL, json=data, headers=headers)
        orders += response.json()["data"]["next_items_page"]["items"]
        cursor = response.json()["data"]["next_items_page"]["cursor"]

    orders_from_deco = []

    for order in orders:
        if order["group"]["id"] == GROUP_ID:
            orders_from_deco.append(order["name"][0:5])

    return orders_from_deco


def write_new_orders(orders):
    """input list
    return boolean

    Take a list of orders from Deco and generate new items on Monday.com
    """

    deco_group = check_deco_group()

    for order in orders:
        try:
            if order["is_priority"]:
                is_priority = "Tassativo"
                print(f"{order['order_id']} priority: {order['is_priority']}")
            else:
                is_priority = "Standard"
                print(f"{order['order_id']} priority: {order['is_priority']}")

            billing_details = order["billing_details"]
            if billing_details["company"] != "":
                customer_name = billing_details["company"]
            else:
                customer_name = f"{billing_details['firstname']} {billing_details['lastname']}"

            if order["job_name"] == "":
                job_name = customer_name
            else:
                job_name = order["job_name"]

            sales_members = ["Fabiano", "Denise", "Gian Marco", "Paolo", ""]

            if order["assigned_to"] is None:
                sales = "Gian Marco"
            elif order["assigned_to"]["firstname"] not in sales_members:
                sales = "Gian Marco"
            else:
                sales = order["assigned_to"]["firstname"]

            if order["shipping_method"]['name'][0:6] == "Ritiro":
                shipping_method = "RITIRO"
                print(f"{order['order_id']} spedizione: {shipping_method}")
            else:
                shipping_method = "SPEDIZIONE"
                print(f"{order['order_id']} spedizione: {shipping_method}")

            item_name = f"{order['order_id']} - {customer_name} - {job_name}"

            query = "mutation ($myItemName: String!, $boardId: ID!, $groupId: String!, $columnVals: JSON!) " \
                    "{ create_item (board_id:$boardId, item_name:$myItemName, " \
                    "group_id:$groupId, column_values:$columnVals) { id } }"
            query_vars = {
                "myItemName": item_name,
                "boardId": int(BOARD_ID),
                "groupId": GROUP_ID,
                "columnVals": json.dumps({
                    "stato_16": sales,
                    "numero_d_ordine": str(order["order_id"]),
                    "nome_cliente": customer_name,
                    "data_dell_ordine": order["date_ordered"][:-19],
                    "data_di_consegna_o_spedizione3": order["date_due"][:-19],
                    "priority": {"label": is_priority},
                    "stato_106": {"label": shipping_method}
                })
            }

        except TypeError:
            print(f"TypeError with order: {order['order_id']}")
            continue

        # Check if the order is already in the deco group
        if str(order["order_id"]) not in deco_group:
            data = {'query': query, 'variables': query_vars}

            response = requests.post(url=API_URL, json=data, headers=headers)

            print(f"Order {order['order_id']} - {customer_name} - {job_name}:")
            print(response.json())
