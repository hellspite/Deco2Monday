import requests
import os
import json

API_URL = "https://api.monday.com/v2"
API_KEY = os.environ["MONDAY_API"]
BOARD_ID = "2241731758"
GROUP_ID = "nuovo_gruppo74198"
headers = {"Authorization": API_KEY}


def test_query():

    query = '{ boards (ids: 2241731758) {name id description columns{id title}} }'

    data = {'query': query}

    response = requests.post(url=API_URL, json=data, headers=headers)

    print(response.json())


def write_new_orders(orders):
    """input list
    return boolean

    Take a list of orders from Deco and generate new items on Monday.com
    """

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

            query = "mutation ($myItemName: String!, $boardId: Int!, $groupId: String!, $columnVals: JSON!) " \
                    "{ create_item (board_id:$boardId, item_name:$myItemName, " \
                    "group_id:$groupId, column_values:$columnVals) { id } }"
            query_vars = {
                "myItemName": job_name,
                "boardId": int(BOARD_ID),
                "groupId": GROUP_ID,
                "columnVals": json.dumps({
                    "numero_d_ordine": str(order["order_id"]),
                    "nome_cliente": customer_name,
                    "data_dell_ordine": order["date_ordered"][:-9],
                    "data_di_consegna_o_spedizione3": order["date_due"][:-9],
                    "priority": {"label": is_priority}
                })
            }

            data = {'query': query, 'variables': query_vars}

            response = requests.post(url=API_URL, json=data, headers=headers)

            print(f"Order {order['order_id']} - {customer_name} - {job_name}:")
            print(response.json())

        except TypeError:
            print(f"TypeError with order: {order['order_id']}")
